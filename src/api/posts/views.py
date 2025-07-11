from fastapi import APIRouter, Depends, Request

from api.auth import ActiveUserDep
from api.auth.service import AuthServiceDep
from api.auth.views import http_bearer
from api.posts.schemas import (
    PostCreateSchema,
    PostReadSchema,
    PostUpdateSchema,
    PostUpdatePartialSchema,
)
from api.posts.service import PostServiceDep
from core.dependencies import PaginationDep
from schemas import PaginationSchema

router = APIRouter(prefix="/posts", tags=["Посты"], dependencies=[Depends(http_bearer)])


@router.post("")
async def create_post(
    active_user: ActiveUserDep,
    post_service: PostServiceDep,
    post_data: PostCreateSchema,
):
    post_id = await post_service.create_post(
        user_id=active_user.id, post_data=post_data
    )
    return {"post_id": post_id}


@router.get("/{post_id}", response_model=PostReadSchema)
async def get_post_by_post_id(
    active_user: ActiveUserDep,
    post_service: PostServiceDep,
    post_id: int,
):
    post = await post_service.get_post_by_post_id(
        user_id=active_user.id, post_id=post_id
    )
    return post


@router.get("", response_model=list[PostReadSchema])
async def get_user_posts(
    active_user: ActiveUserDep,
    post_service: PostServiceDep,
    pagination: PaginationDep,
):
    posts = await post_service.get_posts(user_id=active_user.id, pagination=pagination)
    return posts


@router.put("/{post_id}", response_model=PostReadSchema)
async def update_user_post(
    active_user: ActiveUserDep,
    post_service: PostServiceDep,
    post_data: PostUpdateSchema,
    post_id: int,
):
    post = await post_service.update_post(
        user_id=active_user.id,
        post_id=post_id,
        post_data=post_data,
        partial=False,
    )
    return post


@router.patch("/{post_id}", response_model=PostReadSchema)
async def update_user_post_partially(
    active_user: ActiveUserDep,
    post_service: PostServiceDep,
    post_data: PostUpdatePartialSchema,
    post_id: int,
):
    post = await post_service.update_post(
        user_id=active_user.id,
        post_id=post_id,
        post_data=post_data,
        partial=True,
    )
    return post
