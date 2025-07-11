from aiobcrypt import hashpw_with_salt, checkpw


async def hash_password(password: str) -> str:
    return (await hashpw_with_salt(password.encode())).decode()


async def verify_passwords(password: str, hash_pwd: str) -> bool:
    return await checkpw(password.encode(), hash_pwd.encode())
