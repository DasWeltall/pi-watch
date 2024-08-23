# PiWatch

PiWatch is a powerful Python application that monitors your system's CPU usage, network status, disk space, RAM, and more, all in a modern GUI built with Tkinter.

## Features

- *CPU Usage and Frequency*: Displays the current CPU usage percentage and frequency in MHz.
- *Network Status*: Checks and displays the status of your internet connection.
- *Free Disk Space*: Displays the free disk space in GB.
- *RAM and Swap Usage*: Shows the percentage of RAM and Swap memory used.
- *System Uptime*: Displays the time since the last system boot.
- *Top 4 Processes*: Lists the top 4 processes consuming the most CPU and memory.

## Installation

To install and run the application, follow these steps:

1. *Download and Run the Installation Script*:

    Open your terminal and run the following commands:

    bash
    curl -O https://raw.githubusercontent.com/DasWeltall/pi-watch/main/install.sh
    chmod +x install.sh
    ./install.sh
    

    This script will:
    - Clone the repository from GitHub.
    - Check and install Python and Pip if they are not already installed.
    - Install the required Python packages.
    - Copy the main script to your Desktop.
    - Create a shortcut on your Desktop.
    - Start the application.

2. *Launch the App*:

    Once the script completes, a shortcut named PiWatch will be created on your Desktop. Simply double-click the shortcut to launch the application.

## Requirements

- Python 3.11
- Pip

The installation script will automatically check for these and install them if necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome improvements and new features!

## Support

If you encounter any issues or have questions, feel free to open an issue on the GitHub repository.

---

Thank you for using PiWatch!
