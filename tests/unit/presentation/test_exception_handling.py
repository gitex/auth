import pytest


@pytest.mark.asyncio
async def test_api_handle_infra_exception(client):
    r = await client.get("/")
    assert r.status_code == 200
