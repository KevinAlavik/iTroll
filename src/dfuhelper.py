from itrollutils import clear_screen, print_banner
from device import *
from jailbreak import *
from app_manager import *
from advanced import *
from config import Info, Config
import time
import os

def enter_dfu_mode(udid):
    click.echo(click.style(f"Telling {udid} to enter recovery Mode", fg="cyan"))
    command = ["palera1n", "--enter-recovery"]
    return animate_command(command)


def exit_dfu_mode(udid):
    command = ["palera1n", "--exit-recovery"]
    return animate_command(command)

def animate_command(command):
    # animation = "|/-\\"
    with click.progressbar(length=4, label="Running command (" + " ".join(command) + ")") as progress_bar:
        try:
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            while process.poll() is None:
                progress_bar.update(1)

            output, _ = process.communicate()
            return process.returncode == 0
        except subprocess.CalledProcessError:
            return False
