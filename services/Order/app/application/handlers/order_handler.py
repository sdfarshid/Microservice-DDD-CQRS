import asyncio
import decimal
from typing import List
from uuid import UUID, uuid4

from fastapi import Depends

from app.application.commands.create_order import CreateOrderCommand, OrderItemCommand
from app.domain.order.aggregates.order import Order
from app.domain.order.entities.invoice import Invoice
from app.domain.order.entities.order_item import OrderItem
from app.domain.order.enums.invoice_status import InvoiceStatus
from app.domain.order.enums.item_status import ItemStatus
from app.domain.order.enums.order_status import OrderStatus
from app.infrastructure import message_broker
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.infrastructure.repositories.interface.IOrder_repository import IOrderRepository
from app.infrastructure.repositories.order_repository import OrderRepository
from app.utilities.gateway_client import GatewayClient
from app.utilities.log import DebugError, DebugWarning


class OrderHandler:
    def __init__(self, repository: IOrderRepository = Depends(OrderRepository)):
        self.repository = repository
        self.gateway_client = GatewayClient()
        self.message_broker = message_broker

    async def create(self, command: CreateOrderCommand) -> dict:
        order = None
        try:
            # Calculate total amount with HTTP request to gateway and product
            items = await self._create_order_item_with_fetching_price(command.items)

            # Store order
            order = await self._store_orders(command, items)

            # Store order items
            await self._store_order_items(order.id, items)

            # Store invoice
            invoice = await self._store_invoice(order)

            # 1 - Reserve items just have 1 quantity
            reserved_items = await self.__reserved_products(order.id, items)
            if not reserved_items:
                raise ValueError("No items available to proceed with order")

            payment_response = await self._call_payment(invoice)

            return {
                "invoice": invoice,
                "payment_url": payment_response["payment_url"],

            }
        except Exception as e:
            if order:
                await self.__cansel_order(order)
            raise e

    async def _create_order_item_with_fetching_price(self, items: List[OrderItemCommand]) -> List[OrderItem]:
        total_amount = 0
        order_items = []
        #TODO:: should Using Batch API
        # product_id = [item["product_id"] for item in items]
        # products = await self.gateway_client.get_products_batch(product_ids)
        # product_dict = {product["id"]: product for product in products}

        for item in items:
            product = await self._get_product(item.product_id)
            if product["stock"] < item.quantity:
                raise ValueError(f"Product {product['name']} is out of stock")
            price = product["price"]
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_order=price,
                    status=ItemStatus.PENDING
                )
            )
        return order_items

    async def _get_product(self, product_id: UUID) -> dict:
        try:
            return await self.gateway_client.get_product(product_id)
        except ValueError as error:
            DebugError(f"Unexpected error occurred: {error}")
            raise ValueError(f"Unexpected error occurred: {error}")

    async def _get_product_price(self, product_id: UUID) -> decimal:
        try:
            product = await self._get_product(product_id)
            return 0 if not product["price"] else product["price"]
        except ValueError as error:
            DebugError(f"Unexpected error occurred: {error}")
            raise ValueError(f"Unexpected error occurred: {error}")

    async def _store_invoice(self, order: Order) -> Invoice:
        invoice = OrderMapper.make_invoice_domain(order)
        saved_invoice = await self.repository.add_invoice(invoice)
        return saved_invoice

    async def _store_orders(self, command: CreateOrderCommand, items: List[OrderItem]) -> Order:
        orderAggregate = command.to_order_domain(invoice_id=uuid4(), items=items)
        await self.repository.add_order(orderAggregate)
        return orderAggregate

    async def _store_order_items(self, order_id: UUID, items: List[OrderItem]) -> None:
        order_items = [OrderMapper.to_order_item_orm(item, order_id) for item in items]
        await self.repository.add_order_items_batch(order_items)

    async def __reserved_products(self, order_id: UUID, items: list[OrderItem]) -> bool:
        item_list = [{"product_id": str(item.product_id), "quantity": item.quantity} for item in items]
        #[{"product_id": "uuid", "quantity": int}]
        reserved_any = False
        try:
            response = await self.gateway_client.reserve_products_batch(order_id, item_list)
            DebugWarning(response)
            results = response["results"]  #{"results": [{"product_id": "uuid", "success": true/false} , reserved_any: true/false]}
            for item, result in zip(items, results):
                if result["success"]:
                    reserved_any = True
                else:
                    item.status = ItemStatus.OUT_OF_STOCK
                    await self.repository.update_order_item(item_id=item.id, status=item.status.value)

            return reserved_any
        except ValueError as error:
            DebugError(f"Failed to reserve products: {error}")
            #TODO:: Change Status
            for item in items:
                item.status = ItemStatus.OUT_OF_STOCK
                await self.repository.update_order_item(item_id=item.id, status=item.status.value)
            return False

    async def _call_payment(self, invoice) -> dict :
        try:
            return await  self.gateway_client.initiate_payment(
                invoice_id=invoice.id
            )
        except ValueError as error:
            DebugError(f"Unexpected error during call_payment occurred: {error}")
            raise ValueError(f"Unexpected error occurred: {error}")

    async def __cansel_order(self, order: Order):
        #Step 1 update order Status to CANCELED
        #step 2 update order items to CANCELED
        #step 3 update invoice to  FAILED
        #step 4 Release reserved product
        await self.repository.update_order_status(order.id, OrderStatus.CANCELLED.value)
        await self.repository.update_order_items_status(order.id, OrderStatus.CANCELLED.value)
        await self.repository.update_invoice_status(order.invoice_id, InvoiceStatus.FAILED.value)
        await self.__release_products(order.id,order.items)


    async def check_expired_orders(self):
        expired_invoices = await self.repository.get_expired_pending_invoices()
        for invoice in expired_invoices:
            #TODO:: Should change to Batch
            order = await self.repository.get_orders_by_ids(invoice.order_id)
            await self.__cansel_order(order)


    async def __release_products(self, order_id: UUID, items: list[OrderItem]):
        item_list = [{"product_id": str(item.product_id), "quantity": item.quantity} for item in items]
        #[{"product_id": "uuid", "quantity": int}]
        try:
            response = await self.gateway_client.release_reserved_products_batch(order_id, item_list)
            DebugWarning(response)
        except ValueError as error:
            DebugWarning(f"Failed to release products: {error}")
            return False

