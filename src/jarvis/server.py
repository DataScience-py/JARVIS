"""Create a FastAPI app."""

from fastapi import FastAPI

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
