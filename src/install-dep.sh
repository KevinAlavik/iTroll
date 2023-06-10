#!/bin/bash

if command -v brew &> /dev/null; then
    echo ""
else
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install python3 &> /dev/null

brew install ideviceinstalled &> /dev/null
brew install libimobiledevice &> /dev/null

echo "Installed everything needed"