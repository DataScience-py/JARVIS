"""A comand line of Jarvis."""

import json
import os
import platform
from typing import Any

import requests

FILE_CONFIG = "cli_config.json"

config = {
    "HOST": "127.0.0.1",
    "PORT": 9000,
}


def change_config(key: str, value: str) -> None:
    """
    change_config reset config value.

    Parameters
    ----------
    key : str
        name of config value (IN UPPER)
    value : str
        new value of config

    Returns
    -------
    None
        change global variable (config) and call saver data.
    """
    global config
    config[key] = value
    save_config()


def save_config() -> None:
    """
    save_config to file config.

    Returns
    -------
    None
        Nothing.
    """
    global config
    with open(FILE_CONFIG, "w") as f:
        json.dump(config, f, indent=4)


def load_config() -> None:
    """
    load_config get config from file if file if not exists create new file.

    Use default setting if config is empty.

    Returns
    -------
    None
        Managment file
    """
    global config
    if not os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "w") as f:
            json.dump(config, f)
    with open(FILE_CONFIG, "r") as f:
        temp_config = json.load(f)
        config = config if temp_config == {} else temp_config
    with open(FILE_CONFIG, "w") as f:
        json.dump(config, f)


def help() -> None:
    """
    Help return help string from server and cli config.

    Returns
    -------
    None
        Output to console help information
    """
    print(str(get_from_server("help")))


def get_from_server(url: str) -> Any:
    """
    get_from_server create request to server and return response.

    Parameters
    ----------
    url : str
        realative path to router, when provided

    Returns
    -------
    str
        Response from server
    """
    return requests.get(
        f"http://{config['HOST']}:{config['PORT']}/cli/{url}"
    ).json()


def send_to_server(url: str, command: dict[str, Any]) -> None:
    """
    send_to_server Create post request to server and send command.

    Parameters
    ----------
    url : str
        Relative path to router, when provided
    command : dict
        command to send to server
    """
    requests.post(f"http://{config['HOST']}:{config['PORT']}/{url}", command)


def clear_screen() -> None:
    """
    clear_screen clear screen.

    Returns
    -------
    None
        clear screen
    """
    if platform.system() == "Windows":  # Check, if OS - Windows
        os.system("cls")
    else:  # Для macOS и Linux
        os.system("clear")


def parser(string: str) -> list[str]:
    """
    Parser comand and call it.

    Parameters
    ----------
    string : str
        string to parser

    Returns
    -------
    list[str]
        return list with strings
    """
    pars: list[str] = string.split()
    for i in range(len(pars)):
        if pars[i].startswith("-"):
            if pars[i][1] != "-":
                pars[i] = "-" + pars[i]
            pars[i] = pars[i].upper()
            print(pars[i])
        if pars[i].startswith('"') or pars[i].startswith("'"):
            pars[i] = pars[i][1:]
        if pars[i].endswith('"') or pars[i].endswith("'"):
            pars[i] = pars[i][:-1]

    # Manager for comand

    if pars[0] == "--HELP" or pars[0].lower() == "help":
        if len(pars) == 1:
            help()
        else:
            print("Send long request, need 0 args")
    elif pars[0] == "--PORT":
        if len(pars) == 2:
            change_config("PORT", pars[1])
        else:
            print("Send long request, need 0 args")
    elif pars[0] == "--HOST":
        if len(pars) == 2:
            change_config("HOST", pars[1])
        else:
            print("Send long request, need 1 args")
    elif pars[0] == "clear" or pars[0] == "cls":
        clear_screen()

    return pars


if __name__ == "__main__":
    load_config()

    # start loop for comand line input.
    while (comand := input("Jarvis>")) != "exit":
        parser(comand)
