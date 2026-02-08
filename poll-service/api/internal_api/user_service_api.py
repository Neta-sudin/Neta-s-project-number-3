import httpx
from config.config import Config

config = Config()


async def verify_user_registered(user_id: int) -> dict:
    """
    Verify if a user exists and is registered in the User Service.
    Returns dict with 'exists' and 'is_registered' fields.
    Raises exception if User Service is unavailable.
    """
    url = f"{config.USER_SERVICE_BASE_URL}/users/{user_id}/verify"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return {"exists": False, "is_registered": False}
            raise Exception(f"User Service error: {exc}")
        except httpx.RequestError as exc:
            raise Exception(f"Cannot connect to User Service: {exc}")

