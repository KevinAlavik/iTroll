import subprocess
import os
import sys
import time
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
            domains = (domain for domain in domains)
            command.extend("--domain" + str(domains))
            device_info = subprocess.check_output(command).decode("utf-8")
            device_info_lines = device_info.strip().splitlines()

            device = {}
            for line in device_info_lines:
                key, value = line.split(": ", 1)
                device[key] = value

            devices.append(device)


    except subprocess.CalledProcessError as e:
        print(f"Error retrieving device info: {str(e)}")

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
        print(f"  {Colors.OKGREEN}6) Neofetch{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}7) Alot of info{Colors.ENDC}\n")
        option = input(
            f"{Colors.WARNING}Option (or exit to exit):{Colors.ENDC} ")
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

            activation_state = device_details.get('ActivationState')
            baseband_version = device_details.get('BasebandVersion')
            bluetooth_address = device_details.get(
                'BluetoothAddress')
            firmware_version = device_details.get('FirmwareVersion')
            hardware_model = device_details.get('HardwareModel')
            mlb_serial_number = device_details.get(
                'MLBSerialNumber')
            sim_status = device_details.get('SIMStatus')
            wifi_address = device_details.get('WiFiAddress')

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
            f"{Colors.WARNING}Select jailbreak option (Unc0ver, Palera1n) or exit to exit: {Colors.ENDC}")

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

        elif jailbreak_option.lower() == "exit":
            clear_screen()
            main()
        else:
            print(Colors.FAIL + "Invalid jailbreak option selected." + Colors.ENDC)

    elif option == "3":
        cont = input(
            f"{Colors.WARNING}Do you want to continue (y/n). This will put your phone into DFU/Recovery mode: {Colors.ENDC}")
        if cont.lower() == "n":
            print(
                f"{Colors.OKBLUE}[Action]{Colors.OKGREEN} Cancled {Colors.FAIL}\"recovery_call\"{Colors.ENDC}")
            time.sleep(2)
            clear_screen()
            main()
        elif cont.lower() == "y":
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
                        subprocess.run(["palera1n", "--exit-recovery"],
                                       stdout=open(os.devnull, 'wb'))
                        print(
                            f"{Colors.OKBLUE} [Success] {Colors.OKGREEN} Successfully entered recovery mode!")
                    except subprocess.CalledProcessError as e:
                        print(
                            f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to enter recovery mode: {e}")
                    except Exception as e:
                        print(
                            f"{Colors.WARNING} [Error] {Colors.FAIL}An unexpected error occurred: {e}")
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Colors.WARNING} [Critical Error] {Colors.FAIL}Failed to install or move Palera1n: {e}")
                except Exception as e:
                    print(
                        f"{Colors.WARNING} [Critical Error] {Colors.FAIL}An unexpected error occurred: {e}")
        else:
            print(f"{Colors.FAIL} Invalid input{Colors.ENDC}")
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
    elif option == "7":
        clear_screen()
        alotOfInfo()
    elif option.lower() == "exit":
        clear_screen()
        sys.exit()
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
    device_info = subprocess.check_output(
        ["ideviceinfo", "-u", connected_devices[0]['UniqueDeviceID']]).decode("utf-8")
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

    device_data[1] += f"{'-'*27}{Colors.ENDC}{device_name}"
    device_data[2] += f"{'-'*28}{Colors.ENDC}{device_version}"
    device_data[3] += f"{'-'*35}{Colors.ENDC}{device_model}"
    device_data[4] += f"{'-'*28}{Colors.ENDC}{device_serial}"
    device_data[5] += f"{'-'*38}{Colors.ENDC}{udid}" if udid else ""

    output = '\n'.join(device_data)
    print("")
    print(output)
    print("")


def alotOfInfo():
    connected_devices = get_connected_ios_devices()
    print("-" * 50)
    print(Colors.HEADER + "Device Info" + Colors.ENDC)
    print("")
    for i, device in enumerate(connected_devices):
        device_name = device.get('DeviceName', 'Unknown Device')
        device_version = device.get('ProductVersion', 'Unknown Version')
        print(f"{Colors.WARNING}Device {i + 1}:{Colors.ENDC}")
        print(f"  {Colors.WARNING}Name:{Colors.ENDC} {device_name}")
        print(f"  {Colors.WARNING}Version:{Colors.ENDC} {device_version}")
        print("")

        device_index = input(
            f"{Colors.WARNING}Enter the device number to get more info (or exit to exit):{Colors.ENDC} ")
        if device_index == "exit":
            return

        try:
            device_index = int(device_index) - 1
            selected_device = connected_devices[device_index]
            print("")

            udid = selected_device.get('UniqueDeviceID', '')
            if udid:
                print(f"{Colors.HEADER}UDID:{Colors.ENDC} {udid}")
            else:
                print(f"{Colors.FAIL}UDID not found.{Colors.ENDC}")

            print(
                f"{Colors.HEADER}Device Name:{Colors.ENDC} {selected_device.get('DeviceName')}")
            print(
                f"{Colors.HEADER}Product Type:{Colors.ENDC} {selected_device.get('ProductType')}")
            print(
                f"{Colors.HEADER}Product Version:{Colors.ENDC} {selected_device.get('ProductVersion')}")
            print(
                f"{Colors.HEADER}Build Version:{Colors.ENDC} {selected_device.get('BuildVersion')}")
            print(
                f"{Colors.HEADER}Device Color:{Colors.ENDC} {selected_device.get('DeviceColor')}")
            print(f"{Colors.HEADER}Device Enclosure Color:{Colors.ENDC} {selected_device.get('DeviceEnclosureColor')}")
            print(
                f"{Colors.HEADER}Battery Level:{Colors.ENDC} {selected_device.get('BatteryLevel')}")
            print(
                f"{Colors.HEADER}Serial Number:{Colors.ENDC} {selected_device.get('SerialNumber')}")
            print(
                f"{Colors.HEADER}Phone Number:{Colors.ENDC} {selected_device.get('PhoneNumber')}")
            print(
                f"{Colors.HEADER}IMEI:{Colors.ENDC} {selected_device.get('IMEI')}")
            print(
                f"{Colors.HEADER}MEID:{Colors.ENDC} {selected_device.get('MEID')}")
            print(
                f"{Colors.HEADER}ICCID:{Colors.ENDC} {selected_device.get('ICCID')}")
            print(
                f"{Colors.HEADER}Baseband Version:{Colors.ENDC} {selected_device.get('BasebandVersion')}")
            print(
                f"{Colors.HEADER}Bluetooth Address:{Colors.ENDC} {selected_device.get('BluetoothAddress')}")
            print(
                f"{Colors.HEADER}WiFi Address:{Colors.ENDC} {selected_device.get('WiFiAddress')}")
            print(
                f"{Colors.HEADER}Model Number:{Colors.ENDC} {selected_device.get('ModelNumber')}")
            print(
                f"{Colors.HEADER}Model Name:{Colors.ENDC} {selected_device.get('ModelName')}")
            print(
                f"{Colors.HEADER}Hardware Model:{Colors.ENDC} {selected_device.get('HardwareModel')}")
            print(
                f"{Colors.HEADER}CPU Architecture:{Colors.ENDC} {selected_device.get('CPUArchitecture')}")
            print(
                f"{Colors.HEADER}SIM Carrier Network:{Colors.ENDC} {selected_device.get('SIMCarrierNetwork')}")
            print(
                f"{Colors.HEADER}Carrier Country:{Colors.ENDC} {selected_device.get('CarrierCountry')}")
            print(f"{Colors.HEADER}Carrier Mobile Country Code:{Colors.ENDC} {selected_device.get('CarrierMobileCountryCode')}")
            print(f"{Colors.HEADER}Carrier ISOCountry Code:{Colors.ENDC} {selected_device.get('CarrierISOCountryCode')}")
            print(f"{Colors.HEADER}Carrier Mobile Network Code:{Colors.ENDC} {selected_device.get('CarrierMobileNetworkCode')}")
            print(
                f"{Colors.HEADER}Current MCC:{Colors.ENDC} {selected_device.get('CurrentMCC')}")
            print(
                f"{Colors.HEADER}Current MNC:{Colors.ENDC} {selected_device.get('CurrentMNC')}")
            print(
                f"{Colors.HEADER}Data Roaming Enabled:{Colors.ENDC} {selected_device.get('DataRoamingEnabled')}")
            print(f"{Colors.HEADER}Device Supports Face ID:{Colors.ENDC} {selected_device.get('DeviceSupportsFaceID')}")
            print(f"{Colors.HEADER}Device Supports Touch ID:{Colors.ENDC} {selected_device.get('DeviceSupportsTouchID')}")
            print(f"{Colors.HEADER}Device Supports Proximity Sensor:{Colors.ENDC} {selected_device.get('DeviceSupportsProximitySensor')}")
            print(f"{Colors.HEADER}Device Supports Apple Pay:{Colors.ENDC} {selected_device.get('DeviceSupportsApplePay')}")
            print(f"{Colors.HEADER}Device Supports Telephony:{Colors.ENDC} {selected_device.get('DeviceSupportsTelephony')}")
            print(
                f"{Colors.HEADER}Device Supports NFC:{Colors.ENDC} {selected_device.get('DeviceSupportsNFC')}")
            print(f"{Colors.HEADER}Device Supports Camera:{Colors.ENDC} {selected_device.get('DeviceSupportsCamera')}")
            print(
                f"{Colors.HEADER}Device Supports Siri:{Colors.ENDC} {selected_device.get('DeviceSupportsSiri')}")
            print(f"{Colors.HEADER}Device Supports Siri Shutter:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriShutter')}")
            print(f"{Colors.HEADER}Device Supports Siri Voice ID:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriVoiceID')}")
            print(f"{Colors.HEADER}Device Supports Siri Continuous Dictation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriContinuousDictation')}")
            print(f"{Colors.HEADER}Device Supports Siri Eyes Free:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriEyesFree')}")
            print(f"{Colors.HEADER}Device Supports Car Audio:{Colors.ENDC} {selected_device.get('DeviceSupportsCarAudio')}")
            print(
                f"{Colors.HEADER}Device Supports WiFi:{Colors.ENDC} {selected_device.get('DeviceSupportsWiFi')}")
            print(f"{Colors.HEADER}Device Supports Bluetooth:{Colors.ENDC} {selected_device.get('DeviceSupportsBluetooth')}")
            print(
                f"{Colors.HEADER}Device Supports A2DP:{Colors.ENDC} {selected_device.get('DeviceSupportsA2DP')}")
            print(f"{Colors.HEADER}Device Supports AVRCP:{Colors.ENDC} {selected_device.get('DeviceSupportsAVRCP')}")
            print(f"{Colors.HEADER}Device Supports HID Over GATT Keyboard:{Colors.ENDC} {selected_device.get('DeviceSupportsHIDOverGATTKeyboard')}")
            print(f"{Colors.HEADER}Device Supports HID Over GATT Mouse:{Colors.ENDC} {selected_device.get('DeviceSupportsHIDOverGATTMouse')}")
            print(f"{Colors.HEADER}Device Supports Low Energy Single Mode:{Colors.ENDC} {selected_device.get('DeviceSupportsLowEnergySingleMode')}")
            print(f"{Colors.HEADER}Device Supports Voice Over LTE:{Colors.ENDC} {selected_device.get('DeviceSupportsVoiceOverLTE')}")
            print(
                f"{Colors.HEADER}Device Supports GPS:{Colors.ENDC} {selected_device.get('DeviceSupportsGPS')}")
            print(
                f"{Colors.HEADER}Device Supports VoIP:{Colors.ENDC} {selected_device.get('DeviceSupportsVoIP')}")
            print(f"{Colors.HEADER}Device Supports Apple Music:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleMusic')}")
            print(f"{Colors.HEADER}Device Supports Apple Music Catalog Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleMusicCatalogPlayback')}")
            print(f"{Colors.HEADER}Device Supports Apple Music Radio:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleMusicRadio')}")
            print(f"{Colors.HEADER}Device Supports Apple Music Restricted:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleMusicRestricted')}")
            print(f"{Colors.HEADER}Device Supports Apple Music Subscription:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleMusicSubscription')}")
            print(f"{Colors.HEADER}Device Supports Hearing Aid Audio Equalization:{Colors.ENDC} {selected_device.get('DeviceSupportsHearingAidAudioEqualization')}")
            print(f"{Colors.HEADER}Device Supports Dolby Atmos:{Colors.ENDC} {selected_device.get('DeviceSupportsDolbyAtmos')}")
            print(
                f"{Colors.HEADER}Device Supports TTY:{Colors.ENDC} {selected_device.get('DeviceSupportsTTY')}")
            print(f"{Colors.HEADER}Device Supports Voice Control:{Colors.ENDC} {selected_device.get('DeviceSupportsVoiceControl')}")
            print(f"{Colors.HEADER}Device Supports Accessibility Assistant:{Colors.ENDC} {selected_device.get('DeviceSupportsAccessibilityAssistant')}")
            print(f"{Colors.HEADER}Device Supports Assisted GPS:{Colors.ENDC} {selected_device.get('DeviceSupportsAssistedGPS')}")
            print(f"{Colors.HEADER}Device Supports Emergency SOS:{Colors.ENDC} {selected_device.get('DeviceSupportsEmergencySOS')}")
            print(f"{Colors.HEADER}Device Supports QuickPath:{Colors.ENDC} {selected_device.get('DeviceSupportsQuickPath')}")
            print(f"{Colors.HEADER}Device Supports Carrying Case:{Colors.ENDC} {selected_device.get('DeviceSupportsCarryingCase')}")
            print(f"{Colors.HEADER}Device Supports Stereo Audio:{Colors.ENDC} {selected_device.get('DeviceSupportsStereoAudio')}")
            print(f"{Colors.HEADER}Device Supports Ultra Wide Band:{Colors.ENDC} {selected_device.get('DeviceSupportsUltraWideBand')}")
            print(f"{Colors.HEADER}Device Supports Mobile Subscriber Guide:{Colors.ENDC} {selected_device.get('DeviceSupportsMobileSubscriberGuide')}")
            print(f"{Colors.HEADER}Device Supports Apple Pencil:{Colors.ENDC} {selected_device.get('DeviceSupportsApplePencil')}")
            print(f"{Colors.HEADER}Device Supports Magic Keyboard:{Colors.ENDC} {selected_device.get('DeviceSupportsMagicKeyboard')}")
            print(f"{Colors.HEADER}Device Supports Touch Calibration:{Colors.ENDC} {selected_device.get('DeviceSupportsTouchCalibration')}")
            print(f"{Colors.HEADER}Device Supports True Tone:{Colors.ENDC} {selected_device.get('DeviceSupportsTrueTone')}")
            print(f"{Colors.HEADER}Device Supports Proximity Detection:{Colors.ENDC} {selected_device.get('DeviceSupportsProximityDetection')}")
            print(f"{Colors.HEADER}Device Supports Auto Low Light Video:{Colors.ENDC} {selected_device.get('DeviceSupportsAutoLowLightVideo')}")
            print(f"{Colors.HEADER}Device Supports Extended Dynamic Range:{Colors.ENDC} {selected_device.get('DeviceSupportsExtendedDynamicRange')}")
            print(f"{Colors.HEADER}Device Supports Content Protection:{Colors.ENDC} {selected_device.get('DeviceSupportsContentProtection')}")
            print(f"{Colors.HEADER}Device Supports Spatial Audio:{Colors.ENDC} {selected_device.get('DeviceSupportsSpatialAudio')}")
            print(f"{Colors.HEADER}Device Supports Dolby Vision:{Colors.ENDC} {selected_device.get('DeviceSupportsDolbyVision')}")
            print(f"{Colors.HEADER}Device Supports AirPlay Video:{Colors.ENDC} {selected_device.get('DeviceSupportsAirPlayVideo')}")
            print(f"{Colors.HEADER}Device Supports AirPlay Audio:{Colors.ENDC} {selected_device.get('DeviceSupportsAirPlayAudio')}")
            print(f"{Colors.HEADER}Device Supports HDR Video:{Colors.ENDC} {selected_device.get('DeviceSupportsHDRVideo')}")
            print(f"{Colors.HEADER}Device Supports Haptic Feedback:{Colors.ENDC} {selected_device.get('DeviceSupportsHapticFeedback')}")
            print(f"{Colors.HEADER}Device Supports Tap to Wake:{Colors.ENDC} {selected_device.get('DeviceSupportsTapToWake')}")
            print(f"{Colors.HEADER}Device Supports Night Mode:{Colors.ENDC} {selected_device.get('DeviceSupportsNightMode')}")
            print(f"{Colors.HEADER}Device Supports Night Mode Camera:{Colors.ENDC} {selected_device.get('DeviceSupportsNightModeCamera')}")
            print(f"{Colors.HEADER}Device Supports Time Lapse Video:{Colors.ENDC} {selected_device.get('DeviceSupportsTimeLapseVideo')}")
            print(f"{Colors.HEADER}Device Supports Dual SIM:{Colors.ENDC} {selected_device.get('DeviceSupportsDualSIM')}")
            print(
                f"{Colors.HEADER}Device Supports eSIM:{Colors.ENDC} {selected_device.get('DeviceSupportseSIM')}")
            print(
                f"{Colors.HEADER}Device Supports 5G:{Colors.ENDC} {selected_device.get('DeviceSupports5G')}")
            print(f"{Colors.HEADER}Device Supports 4K Video:{Colors.ENDC} {selected_device.get('DeviceSupports4KVideo')}")
            print(f"{Colors.HEADER}Device Supports 4K Display:{Colors.ENDC} {selected_device.get('DeviceSupports4KDisplay')}")
            print(f"{Colors.HEADER}Device Supports HDR Display:{Colors.ENDC} {selected_device.get('DeviceSupportsHDRDisplay')}")
            print(f"{Colors.HEADER}Device Supports HDR10:{Colors.ENDC} {selected_device.get('DeviceSupportsHDR10')}")
            print(f"{Colors.HEADER}Device Supports Wide Color Display:{Colors.ENDC} {selected_device.get('DeviceSupportsWideColorDisplay')}")
            print(f"{Colors.HEADER}Device Supports DCI P3:{Colors.ENDC} {selected_device.get('DeviceSupportsDCIP3')}")
            print(f"{Colors.HEADER}Device Supports 3D Touch:{Colors.ENDC} {selected_device.get('DeviceSupports3DTouch')}")
            print(f"{Colors.HEADER}Device Supports Variable Refresh Rate:{Colors.ENDC} {selected_device.get('DeviceSupportsVariableRefreshRate')}")
            print(f"{Colors.HEADER}Device Supports HDR10 Plus:{Colors.ENDC} {selected_device.get('DeviceSupportsHDR10Plus')}")
            print(f"{Colors.HEADER}Device Supports Smart HDR:{Colors.ENDC} {selected_device.get('DeviceSupportsSmartHDR')}")
            print(f"{Colors.HEADER}Device Supports Portrait Mode:{Colors.ENDC} {selected_device.get('DeviceSupportsPortraitMode')}")
            print(f"{Colors.HEADER}Device Supports Portrait Lighting:{Colors.ENDC} {selected_device.get('DeviceSupportsPortraitLighting')}")
            print(f"{Colors.HEADER}Device Supports Depth Effect:{Colors.ENDC} {selected_device.get('DeviceSupportsDepthEffect')}")
            print(f"{Colors.HEADER}Device Supports Animoji:{Colors.ENDC} {selected_device.get('DeviceSupportsAnimoji')}")
            print(f"{Colors.HEADER}Device Supports Memoji:{Colors.ENDC} {selected_device.get('DeviceSupportsMemoji')}")
            print(f"{Colors.HEADER}Device Supports Augmented Reality:{Colors.ENDC} {selected_device.get('DeviceSupportsAugmentedReality')}")
            print(f"{Colors.HEADER}Device Supports LiDAR:{Colors.ENDC} {selected_device.get('DeviceSupportsLiDAR')}")
            print(f"{Colors.HEADER}Device Supports AirTag:{Colors.ENDC} {selected_device.get('DeviceSupportsAirTag')}")
            print(f"{Colors.HEADER}Device Supports Express Cards with Power Reserve:{Colors.ENDC} {selected_device.get('DeviceSupportsExpressCardswithPowerReserve')}")
            print(f"{Colors.HEADER}Device Supports Express Mode with Power Reserve:{Colors.ENDC} {selected_device.get('DeviceSupportsExpressModewithPowerReserve')}")
            print(f"{Colors.HEADER}Device Supports Virtualization:{Colors.ENDC} {selected_device.get('DeviceSupportsVirtualization')}")
            print(f"{Colors.HEADER}Device Supports Apple Pay Cash:{Colors.ENDC} {selected_device.get('DeviceSupportsApplePayCash')}")
            print(f"{Colors.HEADER}Device Supports Personal Hotspot:{Colors.ENDC} {selected_device.get('DeviceSupportsPersonalHotspot')}")
            print(f"{Colors.HEADER}Device Supports WiFi Calling:{Colors.ENDC} {selected_device.get('DeviceSupportsWiFiCalling')}")
            print(f"{Colors.HEADER}Device Supports Dual SIM WiFi Calling:{Colors.ENDC} {selected_device.get('DeviceSupportsDualSIMWiFiCalling')}")
            print(f"{Colors.HEADER}Device Supports HD Voice:{Colors.ENDC} {selected_device.get('DeviceSupportsHDVoice')}")
            print(f"{Colors.HEADER}Device Supports Bluetooth Hearing Aid Control:{Colors.ENDC} {selected_device.get('DeviceSupportsBluetoothHearingAidControl')}")
            print(f"{Colors.HEADER}Device Supports HAC M Rating:{Colors.ENDC} {selected_device.get('DeviceSupportsHACMRating')}")
            print(f"{Colors.HEADER}Device Supports HAC T Rating:{Colors.ENDC} {selected_device.get('DeviceSupportsHACTRating')}")
            print(f"{Colors.HEADER}Device Supports AirPrint:{Colors.ENDC} {selected_device.get('DeviceSupportsAirPrint')}")
            print(f"{Colors.HEADER}Device Supports AirDrop:{Colors.ENDC} {selected_device.get('DeviceSupportsAirDrop')}")
            print(f"{Colors.HEADER}Device Supports Family Sharing:{Colors.ENDC} {selected_device.get('DeviceSupportsFamilySharing')}")
            print(f"{Colors.HEADER}Device Supports Find My:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMy')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestions')}")
            print(f"{Colors.HEADER}Device Supports Siri Shortcuts:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriShortcuts')}")
            print(f"{Colors.HEADER}Device Supports Find My Network:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyNetwork')}")
            print(f"{Colors.HEADER}Device Supports iCloud:{Colors.ENDC} {selected_device.get('DeviceSupportsiCloud')}")
            print(f"{Colors.HEADER}Device Supports iCloud Backup:{Colors.ENDC} {selected_device.get('DeviceSupportsiCloudBackup')}")
            print(f"{Colors.HEADER}Device Supports iCloud Drive:{Colors.ENDC} {selected_device.get('DeviceSupportsiCloudDrive')}")
            print(f"{Colors.HEADER}Device Supports iCloud Keychain:{Colors.ENDC} {selected_device.get('DeviceSupportsiCloudKeychain')}")
            print(f"{Colors.HEADER}Device Supports Find My Friends:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyFriends')}")
            print(f"{Colors.HEADER}Device Supports Find My iPhone:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyiPhone')}")
            print(f"{Colors.HEADER}Device Supports Find My iPad:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyiPad')}")
            print(f"{Colors.HEADER}Device Supports Find My Mac:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyMac')}")
            print(f"{Colors.HEADER}Device Supports Find My Device:{Colors.ENDC} {selected_device.get('DeviceSupportsFindMyDevice')}")
            print(f"{Colors.HEADER}Device Supports Activation Lock:{Colors.ENDC} {selected_device.get('DeviceSupportsActivationLock')}")
            print(f"{Colors.HEADER}Device Supports Apple Books:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleBooks')}")
            print(f"{Colors.HEADER}Device Supports Game Center:{Colors.ENDC} {selected_device.get('DeviceSupportsGameCenter')}")
            print(
                f"{Colors.HEADER}Device Supports Siri:{Colors.ENDC} {selected_device.get('DeviceSupportsSiri')}")
            print(f"{Colors.HEADER}Device Supports Spotlight Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSpotlightSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Hands Free:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriHandsFree')}")
            print(f"{Colors.HEADER}Device Supports Siri Voice Control:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriVoiceControl')}")
            print(f"{Colors.HEADER}Device Supports CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Apple TV App:{Colors.ENDC} {selected_device.get('DeviceSupportsAppleTVApp')}")
            print(f"{Colors.HEADER}Device Supports Wallet:{Colors.ENDC} {selected_device.get('DeviceSupportsWallet')}")
            print(
                f"{Colors.HEADER}Device Supports News:{Colors.ENDC} {selected_device.get('DeviceSupportsNews')}")
            print(f"{Colors.HEADER}Device Supports Stocks:{Colors.ENDC} {selected_device.get('DeviceSupportsStocks')}")
            print(f"{Colors.HEADER}Device Supports Voice Memos:{Colors.ENDC} {selected_device.get('DeviceSupportsVoiceMemos')}")
            print(f"{Colors.HEADER}Device Supports Weather:{Colors.ENDC} {selected_device.get('DeviceSupportsWeather')}")
            print(f"{Colors.HEADER}Device Supports Reminders:{Colors.ENDC} {selected_device.get('DeviceSupportsReminders')}")
            print(f"{Colors.HEADER}Device Supports FaceTime:{Colors.ENDC} {selected_device.get('DeviceSupportsFaceTime')}")
            print(f"{Colors.HEADER}Device Supports Podcasts:{Colors.ENDC} {selected_device.get('DeviceSupportsPodcasts')}")
            print(f"{Colors.HEADER}Device Supports Calculator:{Colors.ENDC} {selected_device.get('DeviceSupportsCalculator')}")
            print(f"{Colors.HEADER}Device Supports Compass:{Colors.ENDC} {selected_device.get('DeviceSupportsCompass')}")
            print(f"{Colors.HEADER}Device Supports Voice Control Without Internet:{Colors.ENDC} {selected_device.get('DeviceSupportsVoiceControlWithoutInternet')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Lock Screen:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsLockScreen')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Home Screen:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsHomeScreen')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Lookup:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsLookup')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions News:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsNews')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Photos:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsPhotos')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Reminders:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsReminders')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Safari:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsSafari')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Contacts:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsContacts')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Events:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsEvents')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Music:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsMusic')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Movies:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsMovies')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcuts')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Notes:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsNotes')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Find My:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsFindMy')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Find My Device:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsFindMyDevice')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Find My Network:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsFindMyNetwork')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions App Store:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsAppStore')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Quick Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsQuickActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Automation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsAutomation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Suggestions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsSuggestions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Siri Watch Face:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsSiriWatchFace')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Widgets:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsWidgets')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Proactive Suggestions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsProactiveSuggestions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Donations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsDonations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts User Activities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsUserActivities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts VoIP Calling:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsVoIPCalling')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Payments:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsPayments')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Photos:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsPhotos')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Lists:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsLists')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Notes:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsNotes')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Maps:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsMaps')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Media:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsMedia')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Travel:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsTravel')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Workflows:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsWorkflows')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Health:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsHealth')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Communication:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsCommunication')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Lists and Notes:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsListsandNotes')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Time:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsTime')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Weather:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsWeather')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Wallet:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsWallet')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Contacts:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsContacts')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Proactive Suggestions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsProactiveSuggestions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Notifications:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsNotifications')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMedia')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Playback:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaPlayback')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Search:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaSearch')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Queue:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaQueue')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Remote:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRemote')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Recommendations:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaRecommendations')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Now Playing:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaNowPlaying')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Media Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsMediaMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Utilities:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsUtilities')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Health Fitness:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHealthFitness')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents CarPlay:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCarPlay')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Travel and Navigation:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsTravelandNavigation')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Financial Services:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsFinancialServices')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Edit:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentEdit')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents App Actions:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsAppActions')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Payment Requests:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsPaymentRequests')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Communication and Messaging:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCommunicationandMessaging')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document Read:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentRead')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Lists and Notes Document View:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsListsandNotesDocumentView')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Calendar:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsCalendar')}")
            print(f"{Colors.HEADER}Device Supports Siri Suggestions Shortcuts Intents Home:{Colors.ENDC} {selected_device.get('DeviceSupportsSiriSuggestionsShortcutsIntentsHome')}")
        except:
            print("Error")

if __name__ == "__main__":
    main()