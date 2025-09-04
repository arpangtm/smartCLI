import click
import json
import os
from RAG import RAG_Setup

def questionaire():
    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
            if config["RAG"]:
                return {"setup_success": True}
    enable_RAG = input("Do you want to enable RAG? (y/n): ") == "y"
    if enable_RAG:
        folder = input("Enter the folder (absolute) path: ")
        
        config = {
            "RAG": {
                "enabled": True,
                "folder": folder
            }
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        RAG_Setup(folder)
    else:
        config = {
            "RAG": {
                "enabled": False,
                "folder": ""
            }
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
    
    click.secho("Setup complete", fg='green')
    return {"setup_success": True}
    