import subprocess
import os
import libimobiledevice

class Config:
    bypass_jailbreak_warning = False

# ANSI escape codes for colored output


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def print_banner():
    banner = """
  _ _______        _ _
 (_)__   __|      | | |
  _   | |_ __ ___ | | |
 | |  | | '__/ _ \| | |
 | |  | | | | (_) | | |
 |_|  |_|_|  \___/|_|_|

"""
    print(Colors.OKBLUE + banner + Colors.ENDC)


def get_connected_ios_devices():
    devices = []

    try:
        idevice_list_output = subprocess.check_output(
            ["idevice_id", "-l"]).decode("utf-8")
        udid_list = idevice_list_output.strip().splitlines()

        for udid in udid_list:
            device_info = subprocess.check_output(
                ["ideviceinfo", "-u", udid]).decode("utf-8")
            device_info_lines = device_info.strip().splitlines()

            device = {}
            for line in device_info_lines:
                key, value = line.split(": ", 1)
                device[key] = value

            devices.append(device)

    except subprocess.CalledProcessError as e:
        print(Colors.FAIL +
              f"Error retrieving device info: {str(e)}" + Colors.ENDC)

    return devices


def install_ipa(ipa_path):
    try:
        # Execute the command to install the IPA using the 'ideviceinstaller' tool
        subprocess.check_call(["ideviceinstaller", "-i", ipa_path])
        print(Colors.OKGREEN + "App installation successful." + Colors.ENDC)
    except subprocess.CalledProcessError as e:
        print(Colors.FAIL + f"Error installing app: {str(e)}" + Colors.ENDC)


def main():
    print_banner()
    connected_devices = get_connected_ios_devices()

    if len(connected_devices) > 0:
        print(Colors.HEADER + "Connected Devices:" + Colors.ENDC)
        print("")
        for i, device in enumerate(connected_devices):
            device_name = device.get('DeviceName', 'Unknown Device')
            device_version = device.get(
                'ProductVersion', 'Unknown Version')  # Fix here
            print(
                f"  {Colors.WARNING}{device_name}{Colors.FAIL} · {Colors.OKGREEN}iOS {device_version}{Colors.ENDC}")
            print("")

        print("\n" + Colors.HEADER + "Tools:" + Colors.ENDC)
        print(f"  {Colors.OKGREEN}1) Device Info{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}2) Jailbreak{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}3) Enter Recovery Mode{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}4) Exit Recovery Mode{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}5) App Manager{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}6) Neofetch{Colors.ENDC}\n")
        option = input(f"{Colors.WARNING}Option:{Colors.ENDC} ")
        optionAction(option)
    else:
        print(Colors.FAIL + "No iOS devices connected." + Colors.ENDC)
        print("")
        print(f"{Colors.HEADER} If you are in recovery mode:")
        print(f"  {Colors.OKGREEN}4) Exit Recovery Mode{Colors.ENDC}\n")
        option = input(f"{Colors.WARNING}Option:{Colors.ENDC} ")
        optionAction(option)


def optionAction(option):
    connected_devices = get_connected_ios_devices()
    clear_screen()
    print_banner()

    if option == "1":
        print("-" * 20)
        print(Colors.HEADER + "Device Information:" + Colors.ENDC)
        print("")
        udid_list = [device["UniqueDeviceID"] for device in connected_devices]
        udid = udid_list[0]
        for i, device in enumerate(connected_devices):
            device_info = subprocess.check_output(
                ["ideviceinfo", "-u", device['UniqueDeviceID']]).decode("utf-8")
            device_info_lines = device_info.strip().splitlines()
            device_details = {}

            for line in device_info_lines:
                key, value = line.split(": ", 1)
                device_details[key] = value

            device_name = device_details.get('DeviceName', 'Unknown Device')
            device_version = device_details.get(
                'ProductVersion', 'Unknown Version')
            device_model = device_details.get('ProductType', 'Unknown Model')
            device_serial = device_details.get(
                'SerialNumber', 'Unknown Serial')

            device_color = device_details.get('DeviceColor')
            device_capacity = device_details.get('DeviceCapacity')
            device_battery = device_details.get('BatteryCurrentCapacity')

            print(f"{Colors.OKBLUE}{device_name}{Colors.ENDC}")
            print(
                f"  {Colors.WARNING}iOS: {Colors.OKGREEN}{device_version}{Colors.ENDC}")
            print(f"  {Colors.WARNING}UDID: {Colors.OKGREEN}{udid}{Colors.ENDC}")
            print(
                f"  {Colors.WARNING}Model: {Colors.OKGREEN}{device_model}{Colors.ENDC}")
            print(
                f"  {Colors.WARNING}Serial Number: {Colors.OKGREEN}{device_serial}{Colors.ENDC}")

            if device_color:
                print(
                    f"  {Colors.WARNING}Color: {Colors.OKGREEN}{device_color}{Colors.ENDC}")
            if device_capacity:
                print(
                    f"  {Colors.WARNING}Capacity: {Colors.OKGREEN}{device_capacity} GB{Colors.ENDC}")
            if device_battery:
                print(
                    f"  {Colors.WARNING}Battery: {Colors.OKGREEN}{device_battery}%{Colors.ENDC}")

            activation_state = device_details.get('ActivationState', 'Unknown')
            baseband_version = device_details.get('BasebandVersion', 'Unknown')
            bluetooth_address = device_details.get(
                'BluetoothAddress', 'Unknown')
            firmware_version = device_details.get('FirmwareVersion', 'Unknown')
            hardware_model = device_details.get('HardwareModel', 'Unknown')
            mlb_serial_number = device_details.get(
                'MLBSerialNumber', 'Unknown')
            sim_status = device_details.get('SIMStatus', 'Unknown')
            wifi_address = device_details.get('WiFiAddress', 'Unknown')

            print(
                f" {Colors.WARNING} Activation State: {Colors.OKGREEN}{activation_state}")
            print(
                f" {Colors.WARNING} Baseband Version: {Colors.OKGREEN}{baseband_version}")
            print(
                f" {Colors.WARNING} Bluetooth Address: {Colors.OKGREEN}{bluetooth_address}")
            print(
                f" {Colors.WARNING} Firmware Version: {Colors.OKGREEN}{firmware_version}")
            print(
                f" {Colors.WARNING} Hardware Model: {Colors.OKGREEN}{hardware_model}")
            print(
                f" {Colors.WARNING} MLB Serial Number: {Colors.OKGREEN}{mlb_serial_number}")
            print(f" {Colors.WARNING} SIM Status: {Colors.OKGREEN}{sim_status}")
            print(
                f"  {Colors.WARNING}WiFi Address: {Colors.OKGREEN}{wifi_address}{Colors.ENDC}")

            print("")

    elif option == "2":
        # Jailbreak option
        jailbreak_option = input(
            f"{Colors.WARNING}Select jailbreak option (Unc0ver, Palera1n): {Colors.ENDC}")

        if jailbreak_option.lower() == "unc0ver":
            working_versions = ['11.0', '11.1', '11.2', '11.3', '11.4', '12.0', '12.1', '12.1.1', '12.1.2', '12.1.3',
                                '12.1.4', '12.2', '12.4', '12.4.1', '13.0', '13.3', '13.5', '13.5.1', '13.6', '13.7', '14.0', '14.2', '14.3']

            available_devices = []
            for device in connected_devices:
                device_version = device.get('DeviceVersion')
                if device_version and device_version in working_versions:
                    available_devices.append(device)

            if available_devices or Config.bypass_jailbreak_warning:
                print(
                    f"Using Unc0ver to jailbreak {device.get('DeviceName')} ({device_version}).")
                # installation_success = install_ipa(
                #     "ipas/unc0ver_8.0.2.signed.ipa")
                installation_success = False
                if installation_success:
                    print(
                        f"{Colors.OKBLUE}Successfully installed unc0ver on the device.{Colors.OKGREEN} Now open unc0ver and press 'Jailbreak'!")
                else:
                    print(
                        f"{Colors.WARNING}[Critical Error] {Colors.FAIL}Failed to install unc0ver on the device.")
            else:
                print(
                    Colors.FAIL + f"Error: No connected devices running supported versions found." + Colors.ENDC)

        elif jailbreak_option.lower() == "palera1n":
            working_versions = ['15.0', '15.1', '15.2', '15.3', '15.4', '15.5',
                                '15.6', '15.7', '15.8', '16.0', '16.1', '16.2', '16.3', '16.4']
            working_models = ['iPhone12,1', 'iPhone12,3', 'iPhone12,5',
                              'iPhone13,1', 'iPhone13,2', 'iPhone13,3', 'iPhone13,4']

            available_devices = []
            for device in connected_devices:
                device_version = device.get('DeviceVersion')
                device_model = device.get('HardwareModel')
                if device_version in working_versions and device_model in working_models:
                    available_devices.append(device)

            if available_devices or Config.bypass_jailbreak_warning:
                print(
                    f"Using Palera1n to jailbreak {device.get('DeviceName')} ({device_version}.")

                try:
                    subprocess.run(
                        ["sudo", "mkdir", "-p", "/usr/local/bin"])
                    subprocess.run(
                        ["sudo", "cp", "lib/palera1n-macos-universal", "/usr/local/bin/palera1n"])
                    subprocess.run(
                        ["sudo", "chmod", "+x", "/usr/local/bin/palera1n"])
                    print(
                        f"{Colors.OKBLUE} [Success] {Colors.OKGREEN} Successfully installed palera1n to {Colors.HEADER} PATH {Colors.OKGREEN} will now be continuing {Colors.ENDC}")
                    try:
                        subprocess.run(["palera1n"])
                        print(
                            f"{Colors.OKBLUE} [Success] {Colors.OKGREEN} Successfully jailbreaked {Colors.HEADER} PATH {Colors.OKGREEN} will now be restarting your device!")
                    except subprocess.CalledProcessError as e:
                        print(
                            f"{Colors.WARNING} [Very Critical Error] {Colors.FAIL}Failed to jailbreak: {e}")
                    except Exception as e:
                        print(
                            f"{Colors.WARNING} [Critical Error] {Colors.FAIL}An unexpected error occurred: {e}")
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to install or move Palera1n: {e}")
                except Exception as e:
                    print(
                        f"{Colors.WARNING} [Critical Error] {Colors.FAIL}An unexpected error occurred: {e}")
            else:
                print(
                    Colors.FAIL + f"No connected devices within the supported versions and models found." + Colors.ENDC)

        else:
            print(Colors.FAIL + "Invalid jailbreak option selected." + Colors.ENDC)

    elif option == "3":
        if os.path.isfile("/usr/local/bin/palera1n"):
            subprocess.run(["palera1n", "--enter-recovery"],
                           stdout=open(os.devnull, 'wb'))
        else:
            try:
                subprocess.run(["sudo", "mkdir", "-p", "/usr/local/bin"])
                subprocess.run(
                    ["sudo", "cp", "lib/palera1n-macos-universal", "/usr/local/bin/palera1n"])
                subprocess.run(
                    ["sudo", "chmod", "+x", "/usr/local/bin/palera1n"])
                try:
                    subprocess.run(["palera1n", "--enter-recovery"],
                                   stdout=open(os.devnull, 'wb'))
                    print(
                        f"{Colors.OKBLUE} [Success] {Colors.OKGREEN} Successfully entered recovery mode!")
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Colors.WARNING} [Error] {Colors.FAIL}Failed to enter recovery mode: {e}")
                except Exception as e:
                    print(
                        f"{Colors.WARNING} [Error] {Colors.FAIL}An unexpected error occurred: {e}")
            except subprocess.CalledProcessError as e:
                print(
                    f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to install or move Palera1n: {e}")
            except Exception as e:
                print(
                    f"{Colors.WARNING} [Critical Error] {Colors.FAIL}An unexpected error occurred: {e}")
    elif option == "4":

        if os.path.isfile("/usr/local/bin/palera1n"):
            subprocess.run(["palera1n", "--exit-recovery"],
                           stdout=open(os.devnull, 'wb'))
        else:
            try:
                subprocess.run(["sudo", "mkdir", "-p", "/usr/local/bin"])
                subprocess.run(
                    ["sudo", "cp", "lib/palera1n-macos-universal", "/usr/local/bin/palera1n"])
                subprocess.run(
                    ["sudo", "chmod", "+x", "/usr/local/bin/palera1n"])
                try:
                    subprocess.run(["palera1n", "--exit-recovery"],
                                   stdout=open(os.devnull, 'wb'))
                    print(
                        f"{Colors.OKBLUE} [Success] {Colors.OKGREEN} Successfully exited recovery mode!")
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to exit recovery mode: {e}")
                except Exception as e:
                    print(
                        f"{Colors.WARNING} [Error] {Colors.FAIL}An unexpected error occurred: {e}")
            except subprocess.CalledProcessError as e:
                print(
                    f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to install or move Palera1n: {e}")
            except Exception as e:
                print(
                    f"{Colors.WARNING} [Critical Error] {Colors.FAIL}An unexpected error occurred: {e}")
    elif option == "5":

        clear_screen()
        print_banner()
        udid_list = [device["UniqueDeviceID"] for device in connected_devices]

        if udid_list:
            udid = udid_list[0]
            print(
                f"{Colors.OKBLUE}[Action]{Colors.OKGREEN} Getting apps for UDID: {Colors.WARNING}{udid_list[0]}{Colors.ENDC}")

            try:
                ideviceinstaller_output = subprocess.check_output(
                    ["ideviceinstaller", "-u", udid, "--list-apps"]).decode("utf-8")
                app_list = ideviceinstaller_output.strip().splitlines()

                if app_list:
                    app_info_array = []
                    # Skip the first line with CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
                    for apps in app_list[1:]:
                        app = apps.strip().split()
                        print(Colors.FAIL + "[App] " + Colors.OKBLUE + str(app[0]).replace(",", '') + Colors.ENDC + " · " + Colors.WARNING + str(
                            app[2:]).replace('[', '').replace('\"', '').replace("'", '').replace("]", '').replace(",", '') + Colors.ENDC)
                    print("- - - - - - - - - -")
                    print(
                        f"{Colors.OKGREEN}[Finished]{Colors.OKBLUE} App amount: {Colors.FAIL}{len(app_list) - 1}{Colors.ENDC}")

                else:
                    print("No apps installed.")

            except subprocess.CalledProcessError as e:
                print(f"Error: {str(e)}")
        else:
            print("No connected iOS devices found.")
    elif option == "6":
        clear_screen()
        neofetch()
    else:
        clear_screen()
        print(Colors.FAIL + "Invalid option selected." + Colors.ENDC)
        main()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def neofetch():

    apple_logo = [
        "\033[0;32m                    c.'",
        "\033[0;33m                 ,xNMM.        Device Name",
        "\033[0;31m               .OMMMMo         iOS Version",
        "\033[0;31m               lMM\\\"           Model",
        "\033[0;35m     .;loddo:.  .olloddol;.    Serial Number",
        "\033[0;34m   cKMMMMMMMMMMNWMMMMMMMMMM0:  UDID",
        "\033[0;36m .KMMMMMMMMMMMMMMMMMMMMMMMWd.  ",
        "\033[0;32m XMMMMMMMMMMMMMMMMMMMMMMMX.        ",
        "\033[0;33m;MMMMMMMMMMMMMMMMMMMMMMMM:",
        "\033[0;31m:MMMMMMMMMMMMMMMMMMMMMMMM:",
        "\033[0;31m.MMMMMMMMMMMMMMMMMMMMMMMX.",
        "\033[0;35m kMMMMMMMMMMMMMMMMMMMMMMMMWd.",
        "\033[0;34m 'XMMMMMMMMMMMMMMMMMMMMMMMMMMk",
        "\033[0;32m  'XMMMMMMMMMMMMMMMMMMMMMMMMK.",
        "\033[0;36m    kMMMMMMMMMMMMMMMMMMMMMMd",
        "\033[0;33m     ;KMMMMMMMWXXWMMMMMMMk.",
        "\033[0;34m       \"cooc*\"    \"*coo'\""
    ]

    connected_devices = get_connected_ios_devices()
    udid_list = [device["UniqueDeviceID"] for device in connected_devices]
    udid = udid_list[0]

    # Retrieve device information outside the loop
    device_info = subprocess.check_output(["ideviceinfo", "-u", connected_devices[0]['UniqueDeviceID']]).decode("utf-8")
    device_info_lines = device_info.strip().splitlines()
    device_details = {}
    for line in device_info_lines:
        key, value = line.split(": ", 1)
        device_details[key] = value

    device_name = device_details.get('DeviceName', 'Unknown Device')
    device_version = device_details.get('ProductVersion', 'Unknown Version')
    device_model = device_details.get('ProductType', 'Unknown Model')
    device_serial = device_details.get('SerialNumber', 'Unknown Serial')
    device_color = device_details.get('DeviceColor')
    device_capacity = device_details.get('DeviceCapacity')
    device_battery = device_details.get('BatteryCurrentCapacity')
    device_type = device_details.get('ProductType')

    device_data = []
    for i in range(0, 17):
        if i == 0:
            device_data.append(f"{apple_logo[i]}{' ' * 30}")
        else:
            device_data.append(apple_logo[i])
    
    device_data[1] += f"{Colors.ENDC}{device_name:>20}"
    device_data[2] += f"{Colors.ENDC}{device_version:>11}"
    device_data[3] += f"{Colors.ENDC}{device_model:>23}"
    device_data[4] += f"{Colors.ENDC}{device_serial:>17}"
    device_data[5] += f"{Colors.ENDC}{udid:>39}" if udid else ""

    output = '\n'.join(device_data)
    print("")
    print(output)
    print("")

if __name__ == "__main__":
    main()
