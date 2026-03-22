

<img width="1380" height="752" alt="FLOWCHART PORTSCANNER" src="https://github.com/user-attachments/assets/ae005a4c-cec0-405f-a8b9-b2d08fbe1877" />





# Individuella-projektet

Cybersecurity port scanner project
A multi-threaded port scanner developed in Python for educational purposes. This tool can scan open ports on a target IP address, identify services, and grab banners.

##  Purpose

This project aims to create an automation tool for port scanning that can:
- Identify open ports on a target device
- Grab banner information from known services
- Log all activity for debugging and tracking
- Provide multiple interaction methods (interactive mode and command line)

##  Features

- **Port Scanning** – Scan single or multiple ports on an IP address
- **Multi-threaded** – Uses up to 100 threads for faster scanning
- **Service Detection** – Attempts to identify services running on open ports
- **Banner Grabbing** – Retrieves banner information from ports like 21, 22, 23, 25, 80, 443
- **Logging** – All activity is logged to `port_scanner.log`


### Interactive Mode
- Scan localhost (127.0.0.1)
- Scan router (192.168.1.1)
- Enter custom IP address or domain name
- Test a single specific port

### Command Line Mode

| -t, --target | Target IP address or hostname | -t 192.168.1.1 |
| -p, --ports | Ports to scan (range or list) | -p 1-1024 or -p 80,443,22 |
| -v, --version | Show version information | -v |
| --help-menu | Show help information | --help-menu |

## System Requirements

- **Python:** Version 3.6 or higher
- **Operating System:** Windows, Linux, or macOS
- **Network:** Active network connection
- **Dependencies:** No external libraries required (uses only standard library)

- ### Installation

bash
git clone https://github.com/Halalkid/Individuella-projektet.git
cd Individuella-projektet

<img width="1376" height="768" alt="Flowchart_portscanner" src="https://github.com/user-attachments/assets/3da01b3d-20ed-4850-8e9e-8a67f495cc7e" />
