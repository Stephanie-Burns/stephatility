import ctypes
import sys
import os
import subprocess
from enum import Enum, auto
import platform


import subprocess
import re


class SystemType(Enum):
    LINUX       = auto()
    WINDOWS     = auto()
    MAC         = auto()
    UNKNOWN     = auto()


def check_system() -> SystemType:
    """
    Checks the operating system of the host machine and returns an enum indicating the type.

    Returns:
        SystemType: An enum value representing the operating system (LINUX, WINDOWS, or UNKNOWN).
    """
    system_name = platform.system().lower()

    if 'linux' in system_name:
        return SystemType.LINUX

    elif 'windows' in system_name:
        return SystemType.WINDOWS

    elif 'darwin' in system_name:
        return SystemType.MAC

    else:
        return SystemType.UNKNOWN


def im_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_ip_address(interface_name='Ethernet') -> str:
    """
    Gets the current IP address for the specified network interface.

    Args:
        interface_name (str): The name of the network interface.

    Returns:
        str: The IP address of the network interface, or None if not found.
    """
    system_type = check_system()
    ip_address = None

    if system_type == SystemType.WINDOWS:
        ip_address = get_windows_ip_address(interface_name)
    elif system_type == SystemType.LINUX:
        ip_address = get_linux_ip_address(interface_name)
    elif system_type == SystemType.MAC:
        ip_address = get_mac_ip_address(interface_name)

    return ip_address


def get_windows_ip_address(interface_name: str) -> str:
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    # A simple Regex to extract an IPv4, adjust according to your needs.
    pattern = rf"{interface_name}.*?IPv4 Address[ .:]+([\d.]+)"
    match = re.search(pattern, result.stdout, re.S)
    if match:
        return match.group(1)
    return None


def get_linux_ip_address(interface_name: str) -> str:
    command = f"ip addr show {interface_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    pattern = r"inet (\d+\.\d+\.\d+\.\d+)/"
    match = re.search(pattern, result.stdout)
    if match:
        return match.group(1)
    return None


def get_mac_ip_address(interface_name: str) -> str:
    command = f"ifconfig {interface_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    pattern = r"inet (\d+\.\d+\.\d+\.\d+) "
    match = re.search(pattern, result.stdout)
    if match:
        return match.group(1)
    return None


def set_windows_ip(
    interface_name: str = "Ethernet",
    new_ip: str = "192.168.1.100",
    subnet_mask="255.255.255.0",
    gateway="192.168.1.1"
) -> None:
    command = f"netsh interface ip set address name=\"{interface_name}\" static {new_ip} {subnet_mask} {gateway}"
    os.system(command)


def set_linux_ip(
    interface="eth0",
    new_ip="192.168.1.100",
) -> None:
    command = f"sudo ip addr add {new_ip}/24 dev {interface}"
    subprocess.run(command, shell=True, check=True)

# =====================

print(get_ip_address())

if not im_admin():
    # Re-run self requesting admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    print("I am running as an admin!")

    match check_system():
        case SystemType.WINDOWS:
            set_windows_ip(new_ip='192.168.1.37')
        case SystemType.LINUX:
            set_linux_ip()
