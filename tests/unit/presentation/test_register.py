import faker
import pytest
from httpx import AsyncClient

from src.domain.value_objects import Email

from src.application.uow import UnitOfWork


fake = faker.Faker()


REGISTER_URL = "/register"


def register_data(email: str, password: str):
    return {"email": email, "password": password}


@pytest.mark.asyncio
async def test_register_by_valid_email_and_password(
    client: AsyncClient,
    password: str,
    uow: UnitOfWork,
):
    email = fake.email(domain="example.com")
    r = await client.post(REGISTER_URL, json=register_data(email, password))
    assert r.status_code == 200, r.json()
    assert await uow.accounts.get_by_email(Email(email))
