import os
import json
import platform
import sys

import typer
import deta
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

app = typer.Typer()
console = Console()

# Just setting up path, check is already done in main.py
current_os = platform.system()
if current_os == "Windows":
    data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "mini","detabase")
elif current_os == "Linux":
    data_dir = os.path.join(os.getenv("HOME"), ".config", "mini", "detabase")

# Add config.json to data_dir
config_path = os.path.join(data_dir, "config.json")


@app.command()
def add(project_name: str):
    with open(config_path, "r") as f:
        config = json.load(f)
    if project_name in config["projects"]:
        console.print("Project name already exists!", style="bold red")
        sys.exit(1)
    project_key = Prompt.ask("Enter your project key: ")
    config["projects"][project_name] = project_key
    with open(config_path, "w") as f:
        json.dump(config, f)
    console.print("Project key saved!", style="bold green")



if __name__ == "__main__":
    app()