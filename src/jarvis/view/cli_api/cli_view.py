"""Router for CLI API."""

from fastapi import APIRouter

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
