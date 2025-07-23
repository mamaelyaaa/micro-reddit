import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
async def user_fixture(client):
    user_data = {
        "email": "user@example.com",
        "password": "qwerty123",
        "username": "mamaelyaaa",
        "is_superuser": False,
    }
    resp = await client.post("/api/auth/register", json=user_data)
    assert resp.status_code == 201
    return user_data


@pytest_asyncio.fixture(scope="function")
async def superuser_fixture(client):
    user_data = {
        "email": "admin@example.com",
        "password": "admin123",
        "username": "admin",
        "is_superuser": True,
    }
    resp = await client.post("/api/auth/register", json=user_data)
    assert resp.status_code == 201
    return user_data
