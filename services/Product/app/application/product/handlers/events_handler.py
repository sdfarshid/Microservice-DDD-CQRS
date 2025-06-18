import json
from typing import List
from uuid import UUID

from fastapi import Depends
from kafka import KafkaProducer, KafkaConsumer

from app.config.config import settings
from services.Product.app.infrastructure.repositories.product.product_repository import ProductRepository


class EventsHandler():
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository)):
        self.repository = product_repository
        self.producer = KafkaProducer(
                    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
                    value_serializer=lambda v: json.dumps(v).encode())
        self.consumer = KafkaConsumer(
            'order-events',
            bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
            value_deserializer=lambda m: json.loads(m.decode()),
            auto_offset_reset='latest'
        )



    async def reserve_stock(self, invoice_id: UUID, items: List[dict]) -> bool:
        for item in items:
            product_id = UUID(item["product_id"])
            quantity = item["quantity"]
            product_db = await self.product_repository.get_product_by_id(product_id)
            if not product_db or product_db.stock < quantity:
                return False
            product_db.stock -= quantity
            await self.product_repository.update_product(product_id, product_db.__dict__)

        #  Event StockReserved
        for item in items:
            event = StockReserved(invoice_id=invoice_id, product_id=UUID(item["product_id"]), quantity=item["quantity"], success=True)
            self.producer.send('stock-events', value=event.model_dump())
        return True

    def start_consuming(self):
        for message in self.consumer:
            if "reason" in message.value:  # OrderCancelled
                event = OrderCancelled(**message.value)
                asyncio.run(self._process_cancelled_event(event))
            else:  # OrderCreated
                event = OrderCreated(**message.value)
                asyncio.run(self._process_order_event(event))

    async def _process_order_event(self, event: OrderCreated):
        for item in event.items:
            product_id = UUID(item["product_id"])
            quantity = item["quantity"]
            product_db = await self.product_repository.get_product_by_id(product_id)
            if product_db and product_db.stock >= quantity:
                product_db.stock -= quantity
                await self.product_repository.update_product(product_id, product_db.__dict__)
                stock_updated_event = {"product_id": str(product_id), "quantity": quantity, "action": "decrease"}
                self.producer.send('stock-events', value=stock_updated_event)

    async def _process_cancelled_event(self, event: OrderCancelled):
        invoice_id = event.invoice_id
        orders = await self.repository.get_orders_by_invoice_id(invoice_id)
        for order in orders:
            product_id = order.product_id
            quantity = order.quantity
            product_db = await self.repository.get_product_by_id(product_id)
            if product_db:
                product_db.stock += quantity
                await self.repository.update_product(product_id, product_db.__dict__)
                stock_updated_event = {"product_id": str(product_id), "quantity": quantity, "action": "release"}
                self.producer.send('stock-events', value=stock_updated_event)


