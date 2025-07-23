import pytest


@pytest.mark.asyncio
class TestUserRegister:

    async def test_user_success_register(self, client):
        user_data = {
            "email": "user123@example.com",
            "password": "qwerty123",
            "username": "user",
            "is_superuser": False,
        }
        resp = await client.post("/api/auth/register", json=user_data)
        print(resp.json())
        assert resp.status_code == 201
        return user_data


# @pytest.mark.asyncio
# class TestUserLogin:
#     pass
#
#
# @pytest.mark.asyncio
# class TestUserRefreshOldToken:
#     pass
