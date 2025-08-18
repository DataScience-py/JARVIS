"""Speech-to-text API."""

from fastapi import APIRouter

stt_api_router = APIRouter()


@stt_api_router.post("/stt")
async def stt(text: str) -> None:
    """
    Stt get text from stt api.

    Parameters
    ----------
    text : str
        a text from stt model.
    """
    print(f"{text=}")
