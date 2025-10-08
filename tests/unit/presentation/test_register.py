from http import HTTPStatus

import faker
import pytest
from httpx import AsyncClient

from src.domain.value_objects import Email

from src.application.uow import UnitOfWork

from tests.urls import URLS


INVALID_EMAILS = [
    ('plainaddress', 'missing @'),
    ('@example.com', 'missing local part'),
    ('john.doe@', 'missing domain'),
    ('john..doe@example.com', 'double dot in local'),
    ('.john@example.com', 'local starts with dot'),
    ('john.@example.com', 'local ends with dot'),
    ('jo hn@example.com', 'space in local'),
    ('john,doe@example.com', 'comma in local'),
    ('john@exa mple.com', 'space in domain'),
    ('john@-example.com', "label starts with '-'"),
    ('john@example-.com', "label ends with '-'"),
    ('john@example..com', 'double dot in domain'),
    ('john@example', 'no public TLD'),
    ('john@123', 'numeric host, no TLD'),
]


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
@pytest.mark.parametrize('email', INVALID_EMAILS)
async def test_register_by_invalid_email(client: AsyncClient, password: str, email: str):
    r = await client.post(URLS.register, json=register_data(email, password))
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, r.json()
