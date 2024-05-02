
import ctypes
import sys
import os
import subprocess
import re
from contextlib import contextmanager, redirect_stdout, redirect_stderr


def check_system() -> bool:
    """
    Checks if the operating system is Windows.

    Returns:
        bool: True if the operating system is Windows, otherwise False.
    """
    return os.name == 'nt'


def is_admin() -> bool:
    """
    Checks if the script is running with administrative privileges.

    Returns:
        bool: True if the script is running as an administrator, otherwise False.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def check_ip_availability(ip):
    """ Ping an IP address to check if it's in use. """
    response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.DEVNULL)
    return response.returncode == 0  # Returns True if IP is in use


def get_ip_address(interface_name: str = 'Ethernet') -> str:
    """
    Gets the current IP address for the specified network interface on Windows.

    Args:
        interface_name (str): The name of the network interface.

    Returns:
        str: The IP address of the network interface, or None if not found.
    """
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    pattern = rf"{interface_name}.*?IPv4 Address[ .:]+([\d.]+)"
    match = re.search(pattern, result.stdout, re.S)
    return match.group(1) if match else None


def set_windows_ip(
    interface_name: str = "Ethernet",
    new_ip:         str = "192.168.1.100",
    subnet_mask:    str = "255.255.255.0",
    gateway:        str = "192.168.1.1"
) -> None:
    """
    Sets a new IP address for the specified interface on Windows.

    Args:
        interface_name (str): Name of the interface.
        new_ip (str): New IP address to set.
        subnet_mask (str): Subnet mask for the new IP.
        gateway (str): Default gateway for the new IP.
    """
    if check_ip_availability(new_ip):
        print(f"IP address {new_ip} is already in use on the network.")
        return

    command = f"netsh interface ip set address name=\"{interface_name}\" static {new_ip} {subnet_mask} {gateway}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if result.returncode == 0:
        print(f"IP address changed successfully to {new_ip}.")
    else:
        print(f"Failed to change IP address: {result}")

# =======


@contextmanager
def redirect_output_to_file(file_path):
    """
    A context manager to redirect stdout and stderr to a file.

    Args:
        file_path (str): The path to the file where stdout and stderr will be written.
    """
    try:
        with open(file_path, 'a') as f:
            with redirect_stdout(f), redirect_stderr(f):
                yield
    finally:
        pass


def main():
    if not is_admin():
        print("Not running as admin. Trying to elevate privileges.")
        run_as_admin()

    else:
        new_ip = '192.168.1.37'
        print("I am running as an admin!")
        print(f"Current IP Address: {get_ip_address()}")
        set_windows_ip(new_ip=new_ip)


if __name__ == "__main__":
    with redirect_output_to_file('output.log'):
        main()
