from fastapi import APIRouter

from app.api.modules.users import user_routes

# from app.api.modules import auth, users
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(user_routes.router)