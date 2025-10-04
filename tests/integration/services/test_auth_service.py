from src.services import AuthService


async def test_auth_service():
    service = AuthService()

    await service.login("test", "test")
