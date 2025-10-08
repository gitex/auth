import pytest
from httpx import AsyncClient

from src.domain.entities import Account


@pytest.mark.asyncio
async def test_successful_login(client: AsyncClient, account: Account, password: str):
    response = await client.post(
        "/login",
        json={
            "email": account.email.value,
            "password": password,
        },
    )

    assert response.status_code == 200, response.json()
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
