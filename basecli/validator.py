import os
import json
from pathlib import Path
from typing import Optional
from deta import Base
from deta import Deta

"""
config.json file structure:
{
    "default_project_key": "project_key",
    "projects": {
        "project_name": "project_key"
    }
}
"""

def validate(config_path):
    # Check if it exists
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    config_path = os.path.join(config_path, "config.json")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            # Add default project key
            json.dump({"default_project_key": " ", "projects": {}}, f)
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.decoder.JSONDecodeError:
        console.print("Invalid config file!", style="bold red")
        console.print("Deleting config file...", style="bold red")
        os.remove(config_path)
        sys.exit(1)
    if config["default_project_key"] == " ":
        return (config_path,False)
    elif config["default_project_key"] != " ":
        return (config_path, True)