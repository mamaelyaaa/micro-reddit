from fastapi import APIRouter

from .admin import admin_router
from .auth.views import router as auth_router
from .posts.views import router as posts_router
from .follows.views import router as follows_router
from .feeds.views import router as feed_router

router = APIRouter(prefix="/api")

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(follows_router)
router.include_router(feed_router)
