import click
from itrollutils import clear_screen, print_banner
from config import Info
from functools import partial
from main import main

def unc0ver_jailbreak():
    click.echo(click.style("Unc0ver jailbreak selected.", fg="cyan"))
    # Add code to perform Unc0ver jailbreak

def palera1n_jailbreak():
    click.echo(click.style("palera1n jailbreak selected.", fg="cyan"))
    # Add code to perform palera1n jailbreak


def jailbreak():
    clear_screen()
    print_banner()
    click.echo(click.style(f"iTroll Jailbreak Handler (v{Info.jb_handler_ver})", fg="yellow"))

    options = [
        {"name": "Unc0ver", "function": unc0ver_jailbreak},
        {"name": "Palera1n", "function": palera1n_jailbreak},
        {"name": "Back", "function": main}
    ]

    prompt = "Select a jailbreak tool: "
    choice_options = [option["name"] for option in options]
    numbered_options = [f"{i+1}. {option}" for i, option in enumerate(choice_options)]
    options_text = "\n".join(numbered_options)
    prompt += f"\n{options_text}\n"

    while True:
        try:
            answer = click.prompt(prompt, type=click.IntRange(min=1, max=len(options)))

            if answer == len(options):
                return True

            function = options[answer - 1]["function"]
            clear_screen()
            print_banner()
            if function:
                function()
                click.echo()
            else:
                click.echo(click.style(f"Invalid option: {answer}", fg="red"))

        except click.BadParameter:
            click.echo(click.style("Invalid option. Please enter a number from the list.", fg="red"))