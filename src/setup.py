import click
import os
import platform
import subprocess
import time

def print_banner():
    banner = """
    _ _______        _ _
    (_)__   __|      | | |
    _    | |_ __ ___ | | |
    | |  | | '__/ _ \| | |
    | |  | | | | (_) | | |
    |_|  |_|_|  \___/|_|_|

    """
    click.echo(click.style(banner, fg="green", bold=True))

def print_welcome_message():
    welcome_message = """
    Welcome to iTroll!

    With iTroll you can control your iDevice! Tutorials and links:

    - How to jailbreak using iTroll: https://puffer.is-a.dev/using-itroll-to-jailbreak.html
    - GitHub Repository: https://github.com/kevinalavik/itroll

    Setup:
    """
    click.echo(click.style(welcome_message, fg="white"))
    command = ["sudo", "-v"]

    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(command, stdout=devnull, stderr=subprocess.STDOUT)
        process.communicate()

def save_file():
    directory = "/etc/itroll"
    filename = "setup.json"
    filepath = os.path.join(directory, filename)
    # Write the file using sudo
    subprocess.run(["sudo", "mkdir", "-p", directory])
    subprocess.run(["sudo", "touch", filepath])
    subprocess.run(["sudo", "chmod", "666", filepath])
    with open(filepath, "w") as f:
        f.write("{ finished: true }")

def install_dependencies():
    system = platform.system()
    if system == "Linux":
        distro = platform.linux_distribution()[0].lower()
        if distro in ["debian", "ubuntu"]:
            package_manager = "apt"
            packages = ["libimobiledevice"]
        elif distro in ["fedora", "centos"]:
            package_manager = "dnf"
            packages = ["libimobiledevice"]
        else:
            click.echo("Unsupported Linux distribution. Please install 'libimobiledevice' manually.")
            return

        click.echo(f"Installing 'libimobiledevice' using {package_manager}...")
        command = ["sudo", package_manager, "install", "-y"] + packages

        # Custom loading animation
        animate_command(command)

    elif system == "Darwin":
        click.echo("    Installing 'libimobiledevice' using Homebrew...")
        command = ["brew", "install", "libimobiledevice"]

        # Custom loading animation
        animate_command(command)

    else:
        click.echo("\n    Unsupported operating system. Please install 'libimobiledevice' manually.")

    click.echo("\n    Installing Python 3 and pip3...")
    python_install_command = ["sudo", "apt", "install", "-y", "python3"]
    pip_install_command = ["sudo", "apt", "install", "-y", "python3-pip"]

    # Custom loading animation
    animate_command(python_install_command)
    animate_command(pip_install_command)

    click.echo("\n    Installing Python packages from requirements.txt...")
    pip_packages_command = ["sudo", "pip3", "install", "-r", "requirements.txt"]

    # Custom loading animation
    animate_command(pip_packages_command)

def animate_command(command):
    # Disable command output
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(command, stdout=devnull, stderr=subprocess.STDOUT)

        # Custom loading animation
        animation = "  |/-\\"
        while process.poll() is None:
            for char in animation:
                time.sleep(0.1)
                click.echo("    Running command (" + str(command).replace('[', '').replace(']', '').replace(',', '').replace("'", '') + ") " + char, nl=False)
                click.echo("\b" * len("    Running command (" + str(command).replace('[', '').replace(']', '').replace(',', '').replace("'", '') + ") " + char), nl=False)

        animation = "Done!"
        click.echo("    Running command (" + str(command).replace('[', '').replace(']', '').replace(',', '').replace("'", '') + ") " + animation, nl=False)
        click.echo("\b" * len("    Running command (" + str(command).replace('[', '').replace(']', '').replace(',', '').replace("'", '') + ") " + animation), nl=False)
def setup():
    print_banner()
    print_welcome_message()
    install_dependencies()
    save_file()

    # Wait for the user to press Enter
    click.echo("\n")
    click.pause(info="    Installation completed! Press Enter to continue...")

if __name__ == "__main__":
    setup()
