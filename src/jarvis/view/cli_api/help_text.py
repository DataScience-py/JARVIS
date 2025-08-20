"""Help text."""

import json

# load configure for dynamical server help.

with open("server.json", "r") as f:
    config = json.load(f)

base_url = fr'http://{config["HOST"]}/{config["PORT"]}'

help_text: str = f"""
This is a Help text for the program (JARVIS). Now we read help from server.

this wiil be write about the server.

{base_url}/ - here you can check your connection to the server.
"""
