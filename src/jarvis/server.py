"""Create a FastAPI app."""

from fastapi import FastAPI

from .cli_api import cli_api_router
from .stt_api import stt_api_router

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    """
    Root base path for check connection.

    Returns
    -------
    dict
        A dictionary with a message.

    """
    return {"message": "Hello World"}


app.include_router(cli_api_router)
app.include_router(stt_api_router)
