"""Router for CLI API."""

from fastapi import APIRouter
from pydantic import BaseModel

from jarvis.core import core

from .help_text import help_text

cli_api_router = APIRouter()


@cli_api_router.get("/help")
def cli_help() -> str:
    """
    cli_help Returns the help text for the API.

    Returns
    -------
    str
        help text for the API
    """
    return help_text


class TextRequest(BaseModel):
    """TextRequest."""

    text: str


@cli_api_router.post("/text")
def cli_text(req: TextRequest) -> None:
    """
    cli_text Returns the text for the API.

    Returns
    -------
    None
    """
    core.cli(req.text)
