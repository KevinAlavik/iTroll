import os
import subprocess
import click

def print_banner():
    banner = """
_ _______        _ _
(_)__   __|      | | |
 _   | |_ __ ___ | | |
| |  | | '__/ _ \| | |
| |  | | | | (_) | | |
|_|  |_|_|  \___/|_|_|

    """
    click.echo(click.style(banner, fg="green", bold=True))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
