from typing import List
from uuid import UUID
from fastapi import Depends
from app.domain.order.entities.order_item import OrderItem
from app.utilities.log import DebugWarning

from shared.domain.order.enums.item_status import ItemStatus


class ProductService:
    def __init__(self, gateway_client):
        self.gateway_client = gateway_client


    async def create_order_items(self, items) -> List[OrderItem]:
        order_items = []
        for item in items:
            DebugWarning(item.product_id)

            product = await self.gateway_client.get_product(item.product_id)
            DebugWarning(product)
            if product["stock"] < item.quantity:
                raise ValueError(f"product {product['name']} is out of stock")
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_order=product["price"],
                    status=ItemStatus.PENDING
                )
            )
        return order_items


    async def reserve_products(self, order_id: UUID, items: List[OrderItem]):
        item_list = [{"product_id": str(item.product_id), "quantity": item.quantity} for item in items]
        DebugWarning(item_list)
        await self.gateway_client.reserve_products_batch(order_id, item_list)


    async def release_products(self, order_id: UUID, items: List[OrderItem]):
        item_list = [{"product_id": str(item.product_id), "quantity": item.quantity} for item in items]
        await self.gateway_client.release_reserved_products_batch(order_id, item_list)

