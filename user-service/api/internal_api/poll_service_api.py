import httpx

from config.config import Config

config = Config()


async def delete_user_answers(user_id: int) -> bool:
    url = f"{config.POLL_SERVICE_BASE_URL}/internal/users/{user_id}/answers"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url)
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as exc:
            print(f"Failed to delete answers for user {user_id}: {exc}")
            return False
        except httpx.RequestError as exc:
            print(f"Request error while deleting answers for user {user_id}: {exc}")
            return False

