import os
import json
import platform
import sys

import typer
import deta
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from basecli.validator import validate
import basecli.config as group_config

app = typer.Typer(no_args_is_help=True)
app.add_typer(group_config.app, name="config")
console = Console()

# Get current os
current_os = platform.system()
if current_os == "Windows":
    data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "mini","detabase")
elif current_os == "Linux":
    data_dir = os.path.join(os.getenv("HOME"), ".config", "mini", "detabase")
else:
    console.print("We don't support your OS yet!", style="bold red")
a = validate(data_dir)
config_path, success = a

if not success:
    console.print("No project key / default project key is not set", style="bold red")
    project_name = Prompt.ask("Enter your project name: ")
    project_key = Prompt.ask("Enter your project key: ")
    with open(config_path, "r") as f:
        config = json.load(f)
    config["projects"][project_name] = project_key
    config["default_project_key"] = project_key
    with open(config_path, "w") as f:
        json.dump(config, f)
    console.print("Project key saved!", style="bold green")



@app.command()
def list():
    with open(config_path, "r") as f:
        config = json.load(f)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Project Name", style="dim")
    table.add_column("Project Key", style="dim")
    table.add_row("Default", config["default_project_key"])
    for project_name, project_key in config["projects"].items():
        table.add_row(project_name, project_key)
    console.print(table)

@app.command()
def use(project_name: str):
    with open(config_path, "r") as f:
        config = json.load(f)
    if project_name in config["projects"]:
        config["default_project_key"] = config["projects"][project_name]
        with open(config_path, "w") as f:
            json.dump(config, f)
        console.print("Default project key set!", style="bold green")
    else:
        console.print("Project name not found!", style="bold red")


if __name__ == "__main__":
    app(prog_name="detabase")