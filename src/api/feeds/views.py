from fastapi import APIRouter, Depends

from api.auth import ActiveUserDep
from api.auth.views import http_bearer
from .schemas import FeedReadSchema
from .service import FeedServiceDep

router = APIRouter(prefix="/feed", tags=["Лента"], dependencies=[Depends(http_bearer)])


@router.get("", response_model=list[FeedReadSchema])
async def get_user_events(active_user: ActiveUserDep, feed_service: FeedServiceDep):
    events = await feed_service.get_user_events(user_id=active_user.id)
    return events
