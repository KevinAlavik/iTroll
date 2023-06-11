import click
import time
import subprocess
import os
from itrollutils import clear_screen, print_banner
from main import main

retry_time = 4

def reset():
    global retry_time
    click.echo(click.style("Resetting iTroll...", fg="red"))
    setup_file = "/etc/itroll/setup.json"
    if os.path.exists(setup_file):
        subprocess.run(["sudo", "rm", setup_file])  # Use subprocess to delete the file
        click.echo(click.style("Successfully reset iTroll. Restarting in 0.7 seconds.", fg="green"))
        time.sleep(0.7)
        clear_screen()
        main()  # Call the main function
    else:
        click.echo("iTroll reset: Failed")
        click.echo(click.style(f"Failed to reset iTroll. Retrying in {retry_time} seconds.", fg="red"))
        time.sleep(retry_time)
        clear_screen()
        print_banner()
        retry_time += 1
        reset()

def show_settings():
    clear_screen()
    print_banner()

    options = [
        {"name": "Reset iTroll", "function": reset},
        {"name": "Back", "function": main}
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
                return True

            function = options[answer - 1]["function"]
            clear_screen()
            print_banner()
            if function:
                function()  # Remove the argument 'show_settings' here
                click.echo()
            else:
                click.echo(click.style(f"Invalid option: {answer}", fg="red"))

        except click.BadParameter:
            click.echo(click.style("Invalid option. Please enter a number from the list.", fg="red"))
