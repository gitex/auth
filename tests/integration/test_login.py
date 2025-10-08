from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.domain.entities import Account


@pytest.mark.asyncio
async def test_successful_login(client: AsyncClient, account: Account, password: str):
    """User with valid email and password.

    Should be able authorize and get access and refresh token.
    """
    response = await client.post(
        '/login',
        json={
            'email': account.email.value,
            'password': password,
        },
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
