from http import HTTPStatus

import pytest
from httpx import AsyncClient

from tests import (
    INVALID_EMAILS,
    URLS,
    parse_unprocessable_entity_response,
)


def request_json(email: str, password: str):
    return {'email': email, 'password': password}


async def test_successful_registation(client: AsyncClient, email: str, password: str):
    r = await client.post(URLS.register, json=request_json(email, password))
    assert r.status_code == HTTPStatus.OK.value, r.json()


@pytest.mark.parametrize(('invalid_email', 'reason'), INVALID_EMAILS)
async def test_registration_should_reject_invalid_email(
    client: AsyncClient, invalid_email: str, reason: str, password: str
):
    r = await client.post(URLS.register, json=request_json(invalid_email, password))
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value, reason
    assert parse_unprocessable_entity_response(r).has_error_for_field('email')


# @pytest.mark.parametrize(('invalid_password', 'reason'), INVALID_PASSWORDS)
# async def test_registration_should_reject_invalid_password(
#     client: AsyncClient,
#     invalid_password: str,
#     reason: str,
#     email: str,
# ):
#     r = await client.post(URLS.register, json=request_json(email, invalid_password)) # noqa
#     assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value, reason  # noqa
#     assert parse_unprocessable_entity_response(r).has_error_for_field('password')  # noqa
