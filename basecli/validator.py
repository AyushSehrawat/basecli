import os
import json
import sys
from pathlib import Path
from typing import Optional

from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def validate(config_path: str):
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    config_path = os.path.join(config_path, "config.json")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            # This version is different from the package version
            json.dump({"version": "v1", "default_project_key": " ", "default_base": [], "projects": {}}, f)
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.decoder.JSONDecodeError:
        console.print("JSONDecodeError! Deleting the config file", style="bold red")
        console.print(f"Config Path: {config_path}", style="bold red")
        cont = console.input('Please save your config file if you want to keep it. Press Enter to continue...')
        if cont == "":
            os.remove(config_path)
            console.print("Deleted config file!", style="bold green")
            sys.exit(1)

    try:
        if config["version"] != "v1":
            console.print("Invalid config file!", style="bold red")
            console.print("Deleting config file...", style="bold red")
            saveit = console.input("Do you want to save it?")
            # if y save it as a current time with seconds json file
            if saveit.lower() == "y":
                with open(f"config_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json", "w") as f:
                    json.dump(config, f)
            os.remove(config_path)
            sys.exit(1)
    except KeyError:
        console.print("Invalid config file!", style="bold red")
        console.print("Deleting config file...", style="bold red")
        os.remove(config_path)
        sys.exit(1)

    if config["default_project_key"] == " ":
        return (config_path, False)
    elif config["default_project_key"] != " ":
        return (config_path, True)
