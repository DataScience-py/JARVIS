from fastapi import APIRouter

from .cli_api import cli_api_router
from .stt_api import stt_api_router

api_router = APIRouter()

api_router.include_router(stt_api_router, prefix="/stt", tags=["stt"])
api_router.include_router(cli_api_router, prefix="/cli", tags=["cli"])

__all__ = ["api_router"]
