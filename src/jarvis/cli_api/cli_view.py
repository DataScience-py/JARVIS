"""Router for CLI API."""

from fastapi import APIRouter

from .help_text import help_text

cli_api_router = APIRouter(tags=["cli"])


@cli_api_router.get("/help")
def cli_help() -> str:
    """CLI help."""
    return help_text
