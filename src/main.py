"""Start the server."""

import json
from typing import Any

import uvicorn

from jarvis import app

PATH_CONFIG = "server.json"
config: dict[str, Any] = {
    "HOST": "127.0.0.1",
    "PORT": 9000,
}


def load_config() -> None:
    """Load the configuration."""
    global config
    with open(PATH_CONFIG, "r") as f:
        config = json.load(f)


if __name__ == "__main__":
    load_config()
    uvicorn.run(app, host=config["HOST"], port=config["PORT"])
