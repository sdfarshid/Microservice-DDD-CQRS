import httpx
from uuid import UUID
from typing import Dict, Any, Optional

from app.config.config import settings
from app.utilities.log import DebugError


class GatewayClient:
    def __init__(self):
        self.gateway_url = settings.API_GATEWAY_URL

    async def get_product(self, product_id):
        return await self.call_api(
            method="GET",
            endpoint=f"product/{product_id}",
        )

    async def reserve_products_batch(self, order_id, item_list):
        json_data = {
            "order_id": str(order_id),
            "items": item_list
        }
        return await self.call_api(
            method="POST",
            endpoint="product/reserve",
            json_data=json_data
        )

    async def get_company(self, company_id: UUID) -> Dict[str, Any]:
        response = await self.client.get(f"{self.gateway_url}/companies/{company_id}")
        response.raise_for_status()
        return response.json()

    async def call_api(self,
                       method: str,
                       endpoint: str,
                       json_data: Optional[dict] = None,
                       params: Optional[dict] = None,
                       timeout: float = 10.0
                       ):
        full_url = f"{self.gateway_url}api/v1/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    url=full_url,
                    method=method.upper(),
                    json=json_data,
                    params=params,
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            DebugError(f"HTTP status error occurred: {e} - {full_url}")
            raise ValueError(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            DebugError(f"Network error occurred: {e} - {full_url}")
            raise ValueError(f"Network error occurred: {e}")
        except ValueError as e:
            DebugError(f"Invalid JSON response: {e} - {full_url}")
            raise ValueError(f"Invalid JSON response: {e}")
        except Exception as e:
            DebugError(f"Unexpected error occurred: {e} - {full_url}")
            raise ValueError(f"Unexpected error: {e}")
