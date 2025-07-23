import pytest


@pytest.mark.asyncio
async def test_api_connection(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Api is working!"


@pytest.mark.asyncio
async def test_db_connection(client):
    resp = await client.get("/health-check")
    assert resp.status_code == 200
    assert "PostgreSQL" in resp.json()["detail"]
