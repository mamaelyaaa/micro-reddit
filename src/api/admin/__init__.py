from fastapi import APIRouter
from .auth.views import router as auth_admin_router

admin_router = APIRouter(prefix="/admin", tags=["Админка"])
admin_router.include_router(auth_admin_router)
