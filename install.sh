#!/bin/bash

if ! command -v git &> /dev/null
then
    echo "Git not found. Installing..."
    sudo apt update
    sudo apt install git
fi

# 1. Clone GitHub repository
echo "Cloning repository from GitHub..."
git clone https://github.com/DasWeltall/pi-watch.git
cd pi-watch

# 2. Check and install Python and Pip if needed
echo "Checking for packages..."
if ! command -v python3 &> /dev/null
then
    echo "Python not found. Installing..."
    sudo apt update
    sudo apt install -y python3
fi

if ! command -v pip3 &> /dev/null
then
    echo "Pip not found. Installing..."
    sudo apt install -y python3-pip
fi

# 3. Check and install Tkinter if needed
if ! python3 -c "import tkinter" &> /dev/null
then
    echo "Tkinter not found. Installing..."
    sudo apt install -y python3-tk
fi

# 4. Install required Python packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

echo "All packages installed!"

# 5. Copy script to Desktop
echo "Creating Desktop shortcut..."
mkdir pi-watch
cp piwatch.py ~/pi-watch/PiWatch.py

# 6. Create Desktop shortcut
cat << EOF > ~/Desktop/PiWatch.desktop
[Desktop Entry]
Name=PiWatch
Comment=Monitor CPU and Network Status
Exec=python3 ~/pi-watch/PiWatch.py
Icon=$(pwd)/icon.png
Terminal=false
Type=Application
EOF

chmod +x ~/Desktop/PiWatch.desktop


echo "Starting the program..."
python3 ~/pi-watch/PiWatch.py
