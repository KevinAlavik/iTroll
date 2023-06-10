#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        echo ""
    else
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install python3 &> /dev/null
    brew install ideviceinstaller &> /dev/null
    brew install libimobiledevice &> /dev/null
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 ideviceinstaller libimobiledevice
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 ideviceinstaller libimobiledevice
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 ideviceinstaller libimobiledevice
    else
        echo "Unsupported Linux distribution. Please install the required packages manually."
        exit 1
    fi
fi

echo "Installed everything needed"
