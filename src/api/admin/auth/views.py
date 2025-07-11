from fastapi import APIRouter, Depends, Request

from api.auth.service import AuthServiceDep
from api.auth.users.schemas import UserReadSchema
from api.auth.views import http_bearer
from .schemas import AdminUserUpdateSchema, AdminUserUpdatePartialSchema

router = APIRouter(prefix="/auth", dependencies=[Depends(http_bearer)])


@router.get("/me", response_model=UserReadSchema)
async def get_current_admin(auth_service: AuthServiceDep, request: Request):
    superuser = await auth_service.get_superuser(request)
    return superuser


@router.put("/{user_id}", response_model=UserReadSchema)
async def update_user(
    auth_service: AuthServiceDep,
    user_id: int,
    request: Request,
    update_data: AdminUserUpdateSchema,
):
    await auth_service.get_superuser(request)
    updated_user = await auth_service.update_user(user_id, update_data, partial=False)
    return updated_user


@router.patch("/{user_id}", response_model=UserReadSchema)
async def update_user_partially(
    auth_service: AuthServiceDep,
    user_id: int,
    request: Request,
    update_data: AdminUserUpdatePartialSchema,
):
    await auth_service.get_superuser(request)
    updated_user = await auth_service.update_user(user_id, update_data, partial=True)
    return updated_user
