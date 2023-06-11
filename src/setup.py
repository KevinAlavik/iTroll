import click
import os
import platform
import requests
import subprocess
import time
import zipfile
from itrollutils import clear_screen


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

    With iTroll, you can control your iDevice! Tutorials and links:

    - How to jailbreak using iTroll: https://puffer.is-a.dev/using-itroll-to-jailbreak.html
    - GitHub Repository: https://github.com/kevinalavik/itroll

    Setup:
    """
    click.echo(click.style(welcome_message, fg="white"))
    command = ["sudo", "-v"]

    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            command, stdout=devnull, stderr=subprocess.STDOUT)
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
        architecture = platform.machine()

        if distro in ["debian", "ubuntu"]:
            package_manager = "apt"
            packages = ["libimobiledevice"]
        elif distro in ["fedora", "centos"]:
            package_manager = "dnf"
            packages = ["libimobiledevice"]
        else:
            click.echo(
                "Unsupported Linux distribution. Please install 'libimobiledevice' manually.")
            return

        click.echo(f"Installing 'libimobiledevice' using {package_manager}...")
        command = ["sudo", package_manager, "install", "-y"] + packages

        # Custom loading animation
        animate_command(command)

        # Determine the palera1n release URL based on the architecture
        if architecture == "x86_64":
            palera1n_url = "https://github.com/palera1n/palera1n/releases/download/v2.0.0-beta.7/palera1n-linux-x86_64"
        elif architecture == "x86":
            palera1n_url = "https://github.com/palera1n/palera1n/releases/download/v2.0.0-beta.7/palera1n-linux-x86"
        elif architecture == "arm64":
            palera1n_url = "https://github.com/palera1n/palera1n/releases/download/v2.0.0-beta.7/palera1n-linux-arm64"
        elif architecture == "armel":
            palera1n_url = "https://github.com/palera1n/palera1n/releases/download/v2.0.0-beta.7/palera1n-linux-armel"
        else:
            click.echo(
                "Unsupported architecture. Please install palera1n manually.")
            return

        # Download palera1n
        download_path = "lib/palera1n"
        download_file(palera1n_url, download_path)
        click.echo(f"\n    Download completed: {download_path}")

    elif system == "Darwin":
        click.echo("    Installing 'libimobiledevice' using Homebrew...")
        command = ["brew", "install", "libimobiledevice"]

        # Custom loading animation
        animate_command(command)

        # Download palera1n
        palera1n_url = "https://github.com/palera1n/palera1n/releases/download/v2.0.0-beta.7/palera1n-macos-universal"
        download_path = "lib/palera1n"
        download_file(palera1n_url, download_path)

    else:
        click.echo(
            "\n    Unsupported operating system. Please install 'libimobiledevice' and palera1n manually.")

    click.echo("\n    Installing Python 3 and pip3...")
    python_install_command = ["sudo", "apt", "install", "-y", "python3"]
    pip_install_command = ["sudo", "apt", "install", "-y", "python3-pip"]

    # Custom loading animation
    animate_command(python_install_command)
    animate_command(pip_install_command)

    click.echo("\n    Installing Python packages from requirements.txt...")
    pip_packages_command = ["sudo", "pip3",
                            "install", "-r", "requirements.txt"]

    # Custom loading animation
    animate_command(pip_packages_command)


def animate_command(command):
    # Disable command output
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            command, stdout=devnull, stderr=subprocess.STDOUT)

        # Custom loading animation
        animation = "|/-\\"
        while process.poll() is None:
            for char in animation:
                time.sleep(0.1)
                click.echo("    Running command (" +
                           " ".join(command) + ") " + char, nl=False)
                click.echo("\b" * len("    Running command (" +
                           " ".join(command) + ") " + char), nl=False)

        animation = "Done!"
        click.echo("    Running command (" + " ".join(command) +
                   ") " + animation, nl=False)
        click.echo("\b" * len("    Running command (" +
                   " ".join(command) + ") " + animation), nl=False)


def download_file(url, download_path):
    click.echo(f"\n    Downloading {url}...")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    click.echo("    Making palera1n executable...")
    subprocess.run(["chmod", "+x", download_path])
    click.echo("    palera1n is now executable.")

    palera1n_dest = "/usr/local/bin/palera1n"
    click.echo(f"    Moving palera1n to {palera1n_dest}...")
    subprocess.run(["sudo", "mv", download_path, palera1n_dest])
    click.echo("    palera1n moved successfully.")

    # Remove the lib/palera1n directory
    click.echo(f"    Removing lib/ directory...")
    subprocess.run(["sudo", "rm", "-rf", "lib/"])
    click.echo(f"    {download_path} directory removed.")


def setup():
    clear_screen()
    print_banner()
    print_welcome_message()
    install_dependencies()
    save_file()


if __name__ == "__main__":
    setup()
