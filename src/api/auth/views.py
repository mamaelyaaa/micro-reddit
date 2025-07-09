from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    status,
)
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)

from core import settings
from .jwt.schemas import BearerResponseSchema
from .service import AuthServiceDep
from .users.schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
    UserUpdatePartialSchema,
)

router = APIRouter(prefix="/auth", tags=["Авторизация"])

http_bearer = HTTPBearer(auto_error=False)
oauth_scheme = OAuth2PasswordBearer(tokenUrl=settings.jwt.token_url, auto_error=False)


@router.post(
    "/register",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(auth_service: AuthServiceDep, user_data: UserCreateSchema):
    user_id = await auth_service.register_user(user_data)
    return user_id


@router.post("/login", response_model=BearerResponseSchema)
async def login_user(
    auth_service: AuthServiceDep, user_data: UserCreateSchema, response: Response
):
    access_token = await auth_service.login_user(user_data, response)
    return access_token


@router.get("/refresh", response_model=BearerResponseSchema)
async def refresh_access_token(auth_service: AuthServiceDep, request: Request):
    new_access_token = await auth_service.refresh_token(request)
    return new_access_token


@router.get("/me", response_model=UserReadSchema, dependencies=[Depends(http_bearer)])
async def get_current_user(auth_service: AuthServiceDep, request: Request):
    current_user = await auth_service.get_active_user(request)
    return current_user


@router.patch("/me", response_model=UserReadSchema, dependencies=[Depends(http_bearer)])
async def current_user_partial_update(
    auth_service: AuthServiceDep, request: Request, update_data: UserUpdatePartialSchema
):
    current_user = await auth_service.get_active_user(request)
    return current_user


@router.put("/me", response_model=UserReadSchema, dependencies=[Depends(http_bearer)])
async def current_user_update(
    auth_service: AuthServiceDep, request: Request, update_data: UserUpdateSchema
):
    current_user = await auth_service.get_active_user(request)
    return current_user
