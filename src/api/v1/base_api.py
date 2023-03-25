from fastapi import APIRouter

from api.v1.short_link_api import router_link

api_router = APIRouter()
api_router.include_router(router_link, prefix="/shorten", tags=["Short link"])
