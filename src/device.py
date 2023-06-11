import subprocess
import click
from itrollutils import clear_screen, print_banner
from config import Info

def get_connected_ios_devices():
    devices = []

    try:
        idevice_list_output = subprocess.check_output(["idevice_id", "-l"]).decode("utf-8")
        udid_list = idevice_list_output.strip().splitlines()

        domains = [
            "com.apple.disk_usage",
            "com.apple.disk_usage.factory",
            "com.apple.mobile.battery",
            "com.apple.iqagent",
            "com.apple.purplebuddy",
            "com.apple.PurpleBuddy",
            "com.apple.mobile.chaperone",
            "com.apple.mobile.third_party_termination",
            "com.apple.mobile.lockdownd",
            "com.apple.mobile.lockdown_cache",
            "com.apple.xcode.developerdomain",
            "com.apple.international",
            "com.apple.mobile.data_sync",
            "com.apple.mobile.tethered_sync",
            "com.apple.mobile.mobile_application_usage",
            "com.apple.mobile.backup",
            "com.apple.mobile.nikita",
            "com.apple.mobile.restriction",
            "com.apple.mobile.user_preferences",
            "com.apple.mobile.sync_data_class",
            "com.apple.mobile.software_behavior",
            "com.apple.mobile.iTunes.SQLMusicLibraryPostProcessCommands",
            "com.apple.mobile.iTunes.accessories",
            "com.apple.mobile.internal",
            "com.apple.mobile.wireless_lockdown",
            "com.apple.fairplay",
            "com.apple.iTunes",
            "com.apple.mobile.iTunes.store",
            "com.apple.mobile.iTunes"
        ]
        for udid in udid_list:
            command = ["ideviceinfo", "-u", udid]
            # command.extend(["-q " + str(domain) for domain in domains])
            device_info = subprocess.check_output(command).decode("utf-8")
            device_info_lines = device_info.strip().splitlines()

            device = {}
            for line in device_info_lines:
                key, value = line.split(": ", 1)
                device[key] = value

            devices.append(device)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error retrieving device info: {str(e)}", fg="red"))

    return devices


def device_info():
    devices = get_connected_ios_devices()
    idevice_list_output = subprocess.check_output(["idevice_id", "-l"]).decode("utf-8")
    udid_list = idevice_list_output.strip().splitlines()
    udid = udid_list[0]
    if len(devices) > 0:
        click.echo(click.style("Connected Device", fg="cyan"))
        click.echo()
        for i, device in enumerate(devices):
            device_name = device.get('DeviceName')
            device_version = device.get('ProductVersion')
            device_serial = device.get('SerialNumber')
            click.echo(click.style(f"  {device_name} · iOS {device_version}", fg="magenta", bold=True))
            click.echo(click.style(f"  \u2514\u2500\u2500 Info:", fg="magenta"))
            click.echo(click.style(f"      \u2514\u2500\u2500 UDID: {udid}", fg="magenta"))
            click.echo(click.style(f"      \u2514\u2500\u2500 Serial Number: {device_serial}", fg="magenta"))
            # click.echo(click.style(f"  \u2514\u2500\u2500 Info2:", fg="magenta"))

            click.echo()

def connected_devices():
    device_info()

def enter_dfu():
    devices = get_connected_ios_devices()
    if len(devices) > 0:
        udid = devices[0].get("UniqueDeviceID")
        click.echo(click.style(f"Telling {udid} to enter DFU/Recovery Mode", fg="cyan"))
        # Add code to enter DFU/Recovery mode
        enter_dfu_mode()
    else:
        click.echo(click.style("No connected devices found.", fg="red"))


def exit_dfu():
    click.echo(click.style("Exiting DFU/Recovery Mode", fg="cyan"))
    # Add code to exit DFU/Recovery mode
    exit_dfu_mode()


if __name__ == "__main__":
    connected_devices()
