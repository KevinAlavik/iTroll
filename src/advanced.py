import click
from itrollutils import clear_screen, print_banner
from config import Info
from device import get_connected_ios_devices
from main import main

def enter_dfu():
    connected_devices = get_connected_ios_devices()
    if connected_devices:
        udid_list = [device["UniqueDeviceID"] for device in connected_devices]
        udid = udid_list[0]
        click.echo(click.style(f"Telling {udid} to enter DFU/Recovery Mode", fg="cyan"))
        # Add code to enter DFU/Recovery mode
    else:
        click.echo(click.style("No connected devices found.", fg="red"))


def exit_dfu():
    click.echo(click.style("Exiting DFU/Recovery Mode", fg="cyan"))
    # Add code to exit DFU/Recovery mode


def advanced():
    clear_screen()
    print_banner()

    options = [
        {"name": "Enter DFU/Recovery Mode", "function": enter_dfu},
        {"name": "Exit DFU/Recovery Mode", "function": exit_dfu},
        {"name": "Back", "function": main}
    ]

    prompt = "Select an advanced function: "
    choice_options = [option["name"] for option in options]
    numbered_options = [f"{i+1}. {option}" for i, option in enumerate(choice_options)]
    options_text = "\n".join(numbered_options)
    prompt += f"\n{options_text}\n"

    try:
        answer = click.prompt(prompt, type=click.IntRange(min=1, max=len(options)))

        function = options[answer - 1]["function"]
        clear_screen()
        print_banner()
        if function:
            function()
            click.echo()
        else:
            click.echo(click.style(f"Invalid option: {answer}", fg="red"))
        
        return True 

    except click.BadParameter:
        click.echo(click.style("Invalid option. Please enter a number from the list.", fg="red"))
