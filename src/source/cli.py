import requests
import os
import json
import platform

FILE_CONFIG = "cli_config.json"

config = {
    "HOST": "127.0.0.1",
    "PORT": 9000,
}


def change_config(key: str, value: str) -> None:
    config[key] = value
    save_config(config)

def save_config(config: dict) -> None:
    with open(FILE_CONFIG, "w") as f:
        json.dump(config, f, indent=4)


def load_config() -> dict:
    global config
    if not os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "w") as f:
            json.dump(config, f)
    with open(FILE_CONFIG, "r") as f:
        temp_config = json.load(f)
        config = config if temp_config == {} else temp_config
    with open(FILE_CONFIG, "w") as f:
        json.dump(config, f)
        

def help() -> str:
    server_help = get_from_server("help")
    return server_help

def get_from_server(url: str) -> str:
    return requests.get(f"http://{config['HOST']}:{config['PORT']}/{url}").text

def send_to_server(url: str, command: dict) -> None:
    print(f"send to server, url: {url}, command: {command}")
    requests.post(f"http://{config['HOST']}:{config['PORT']}/{url}", command)

def clear_screen():
    """
    Очищает экран консоли в зависимости от операционной системы.
    """
    if platform.system() == "Windows": # Проверяем, если ОС - Windows
        os.system('cls')
    else: # Для macOS и Linux
        os.system('clear')

def parser(string: str) -> list[str]:
    """
    parser comand for send to Jarvis server

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
        if pars[i].startswith("\"") or pars[i].startswith("'"):
            pars[i] = pars[i][1:]
        if pars[i].endswith("\"") or pars[i].endswith("'"):
            pars[i] = pars[i][:-1]

    if pars[0] == "--help" or pars[0] == "help":
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


load_config()
while (comand := input("Jarvis>")) != "exit":
    parser(comand)
