from http import HTTPStatus

import faker
import pytest
from httpx import AsyncClient

from src.domain.value_objects import Email

from src.application.uow import UnitOfWork

from tests import INVALID_EMAILS, URLS


def register_data(email: str, password: str):
    return {'email': email, 'password': password}


@pytest.mark.asyncio
async def test_register_by_valid_email_and_password(
    client: AsyncClient,
    password: str,
    uow: UnitOfWork,
    faker: faker.Faker,
):
    email = faker.email()
    r = await client.post(URLS.register, json=register_data(email, password))
    assert r.status_code == HTTPStatus.OK, r.json()
    assert await uow.accounts.get_by_email(Email(email))


@pytest.mark.asyncio
@pytest.mark.parametrize(('email', 'reason'), INVALID_EMAILS)
async def test_register_by_invalid_email(
    client: AsyncClient, password: str, email: str, reason: str
):
    r = await client.post(URLS.register, json=register_data(email, password))
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, reason
