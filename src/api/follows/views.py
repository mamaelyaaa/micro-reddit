from fastapi import APIRouter, status, Depends

from api.auth import ActiveUserDep
from api.auth.views import http_bearer
from api.follows.service import FollowsServiceDep
from schemas import BaseResponseSchema

router = APIRouter(
    prefix="/follows", tags=["Подписки"], dependencies=[Depends(http_bearer)]
)


@router.post(
    "/subscribe", status_code=status.HTTP_201_CREATED, response_model=BaseResponseSchema
)
async def subscribe_user(
    active_user: ActiveUserDep, follows_service: FollowsServiceDep, target_id: int
):
    await follows_service.subscribe_user(
        cur_user_id=active_user.id, target_id=target_id
    )
    return BaseResponseSchema(
        detail=f"Пользователь успешно подписался на {target_id = }"
    )


@router.delete(
    "/unsubscribe",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsubscribe_user(
    active_user: ActiveUserDep, follows_service: FollowsServiceDep, target_id: int
):
    await follows_service.unsubscribe_user(
        cur_user_id=active_user.id, target_id=target_id
    )
    return
