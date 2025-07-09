from fastapi import APIRouter, Depends, Request

from api.auth.service import AuthServiceDep
from api.auth.users.schemas import (
    UserReadSchema,
    UserUpdateSchema,
    UserUpdatePartialSchema,
)
from api.auth.views import http_bearer

router = APIRouter(
    prefix="/admin", tags=["Админка"], dependencies=[Depends(http_bearer)]
)


@router.get("/auth/me", response_model=UserReadSchema)
async def get_current_admin(auth_service: AuthServiceDep, request: Request):
    superuser = await auth_service.get_superuser(request)
    return superuser


@router.put("/auth/{user_id}", response_model=UserReadSchema)
async def update_user(
    auth_service: AuthServiceDep,
    user_id: int,
    request: Request,
    update_data: UserUpdateSchema,
):
    await auth_service.get_superuser(request)
    updated_user = await auth_service.update_user(user_id, update_data, partial=False)
    return updated_user


@router.patch("/auth/{user_id}", response_model=UserReadSchema)
async def update_user_partially(
    auth_service: AuthServiceDep,
    user_id: int,
    request: Request,
    update_data: UserUpdatePartialSchema,
):
    await auth_service.get_superuser(request)
    updated_user = await auth_service.update_user(user_id, update_data, partial=True)
    return updated_user
