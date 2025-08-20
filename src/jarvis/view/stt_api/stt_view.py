"""Speech-to-text API."""

from fastapi import APIRouter

from jarvis.core import core

stt_api_router = APIRouter()


@stt_api_router.post("/text")
async def stt(text: str) -> None:
    """
    Stt get text from stt api.

    Parameters
    ----------
    text : str
        a text from stt model.
    """
    core.stt(text)
