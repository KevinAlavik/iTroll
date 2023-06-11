import click
from itrollutils import clear_screen, print_banner
from config import Info
from device import get_connected_ios_devices
from dfuhelper import enter_dfu_mode, exit_dfu_mode
from main import main

def enter_dfu():
    connected_devices = get_connected_ios_devices()
    if connected_devices:
        click.echo(click.style("Connected devices:", fg="yellow"))
        for device in connected_devices:
            click.echo(f"- {device['UniqueDeviceID']}")
        click.echo()

        device_count = len(connected_devices)
        if device_count > 1:
            click.echo(click.style(f"Multiple devices are connected. Please choose a device:", fg="cyan"))
            udid_list = [device["UniqueDeviceID"] for device in connected_devices]
            for i, udid in enumerate(udid_list):
                click.echo(f"{i+1}. {udid}")
            device_index = click.prompt("Enter the device number", type=click.IntRange(min=1, max=device_count)) - 1
            udid = udid_list[device_index]
        else:
            udid = connected_devices[0]["UniqueDeviceID"]

        enter_dfu_mode(udid)
        click.echo(click.style("Successfully entered recovery mode.", fg="green"))

        exit_dfu_option = click.confirm(click.style("Do you want to exit recovery mode now?", fg="cyan"))
        if exit_dfu_option:
            click.echo(click.style("Exiting recovery mode...", fg="cyan"))
            exit_dfu_mode(udid)
            click.echo(click.style("Successfully exited recovery mode.", fg="green"))
    else:
        click.echo(click.style("No connected devices found.", fg="red"))

def exit_dfu():
    connected_devices = get_connected_ios_devices()
    if connected_devices:
        click.echo()

        device_count = len(connected_devices)
        if device_count > 1:
            click.echo(click.style(f"Multiple devices are connected. Please choose a device:", fg="cyan"))
            udid_list = [device["UniqueDeviceID"] for device in connected_devices]
            for i, udid in enumerate(udid_list):
                click.echo(f"{i+1}. {udid}")
            device_index = click.prompt("Enter the device number", type=click.IntRange(min=1, max=device_count)) - 1
            udid = udid_list[device_index]
        else:
            udid = connected_devices[0]["UniqueDeviceID"]

        click.echo(click.style("Exiting recovery mode...", fg="cyan"))
        exit_dfu_mode(udid)
        click.echo(click.style("Successfully exited recovery mode.", fg="green"))
    else:
        click.echo(click.style("Exiting recovery mode...", fg="cyan"))
        exit_dfu_mode(0)
        click.echo(click.style("Successfully exited recovery mode.", fg="green"))

def advanced():
    clear_screen()
    print_banner()

    options = [
        {"name": "Enter recovery Mode", "function": enter_dfu},
        {"name": "Exit recovery Mode", "function": exit_dfu},
        {"name": "Back", "function": main}
    ]

    prompt = "Select an option: "
    choice_options = [option["name"] for option in options]
    numbered_options = [f"{i+1}. {option}" for i, option in enumerate(choice_options)]
    options_text = "\n".join(numbered_options)
    prompt += f"\n{options_text}\n"

    try:
        answer = click.prompt(prompt, type=click.IntRange(min=1, max=len(options)))

        function = options[answer - 1]["function"]
        clear_screen()
        print_banner()
        function()  # Call the selected function

        if function != main:  # Don't call main() if "Back" option is selected
            return True

    except click.BadParameter:
        click.echo(click.style("Invalid option. Please enter a number from the list.", fg="red"))
