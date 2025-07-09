from fastapi import APIRouter

from .auth.views import router as auth_router
from .admin.views import router as admin_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(admin_router)
