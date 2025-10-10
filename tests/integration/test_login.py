from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.domain.entities import Account

from src.bootstrap import AuthContainer

from tests import INVALID_EMAILS, URLS, parse_unprocessable_entity_response


def request_json(email: str, password: str) -> dict[str, str]:
    return {'email': email, 'password': password}


async def test_successful_login(
    client: AsyncClient, account: Account, password: str, container: AuthContainer
):
    """User with valid email and password.

    Should be able authorize and get access and refresh token.
    """

    response = await client.post(
        URLS.login,
        json=request_json(account.email.value, password),
    )
    assert response.status_code == HTTPStatus.OK.value, response.json()

    access_token = response.json().get('access_token', None)
    refresh_token = response.json().get('refresh_token', None)
    assert access_token
    assert refresh_token

    # TODO: add token validation to be sure, that returned tokens are not
    #   just some strings


@pytest.mark.parametrize(('invalid_email', 'reason'), INVALID_EMAILS)
async def test_login_should_reject_invalid_email(
    client: AsyncClient, password: str, invalid_email: str, reason: str
):
    """User with invalid email."""

    r = await client.post(
        URLS.login,
        json=request_json(invalid_email, password),
    )

    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value, reason
    assert parse_unprocessable_entity_response(r).has_error_for_field('email')


@pytest.mark.asyncio
async def test_login_should_reject_incorrect_password(
    client: AsyncClient, account: Account, password: str
):
    """Registered user with wrong password."""

    incorrect_password = 'notcorrectpassword'
    assert incorrect_password != password  # "password"

    r = await client.post(
        URLS.login,
        json=request_json(account.email.value, incorrect_password),
    )

    assert r.status_code == HTTPStatus.BAD_REQUEST.value, r.json()
