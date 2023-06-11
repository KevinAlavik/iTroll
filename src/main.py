import click
import sys
import os
from functools import partial

from device import connected_devices
from itrollutils import print_banner
from config import Info
from setup import setup

def is_setup_completed():
    return os.path.exists("/etc/itroll/setup.json")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

@click.command()
def main():
    from advanced import advanced
    from app_manager import app_manager
    from jailbreak import jailbreak
    from settings import show_settings

    if not is_setup_completed():
        setup()

    clear_screen()
    print_banner()
    click.echo(click.style(f"iTroll v{Info.version[0]}", fg="blue", bold=True))
    connected_devices()
    click.echo()
    options = [
        {"name": "Jailbreak", "function": jailbreak},
        {"name": "App Manager", "function": app_manager},
        {"name": "Advanced", "function": advanced},
        {"name": "Settings", "function": show_settings},
        {"name": "Exit", "function": sys.exit}
    ]

    prompt = "Select an option: "
    choice_options = [option["name"] for option in options]
    numbered_options = [f"{i+1}. {option}" for i, option in enumerate(choice_options)]
    options_text = "\n".join(numbered_options)
    prompt += f"\n{options_text}\n"

    while True:
        try:
            answer = click.prompt(prompt, type=click.IntRange(min=1, max=len(options)))

            if answer == len(options):
                click.echo(click.style(f"Exiting iTroll v{Info.version[0]}", fg="red", bold=True))
                break

            function = options[answer - 1]["function"]
            clear_screen()
            print_banner()
            function()
            click.echo()

        except click.BadParameter:
            click.echo(click.style("Invalid option. Please enter a number from the list.", fg="red"))

if __name__ == "__main__":
    main()
    connected_devices()
