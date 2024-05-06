
import ctypes
import sys
import subprocess
import re
from typing import Optional
from contextlib import contextmanager, redirect_stdout, redirect_stderr


class WindowsIPManager:
    def __init__(self, interface_name: str = 'Ethernet') -> None:
        self._interface_name: str = interface_name
        self._current_ip: Optional[str] = None
        self.update_current_ip()

    @property
    def current_ip(self) -> Optional[str]:
        """Get the current IP address."""
        return self._current_ip

    @current_ip.setter
    def current_ip(self, value: str) -> None:
        if not self.check_ip_availability(value):
            self._current_ip = value
            print(f"IP address set to {value}")
        else:
            print(f"IP address {value} is already in use. No change applied.")

    @property
    def interface_name(self) -> str:
        """Get the name of the network interface."""
        return self._interface_name

    @interface_name.setter
    def interface_name(self, value: str) -> None:
        print(f"Changing interface from {self._interface_name} to {value}")
        self._interface_name = value
        self.update_current_ip()

    @staticmethod
    def is_admin() -> bool:
        """Check if the current script is running as an administrator."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def check_ip_availability(ip: str) -> bool:
        """Check if the given IP address is in use on the network."""
        response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.DEVNULL)
        return response.returncode == 0

    def run_as_admin(self) -> None:
        """Attempt to restart the program with administrative privileges."""
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    def update_current_ip(self) -> None:
        """Update the current IP address from the system configuration."""
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        pattern = rf"{self._interface_name}.*?IPv4 Address[ .:]+([\d.]+)"
        match = re.search(pattern, result.stdout, re.S)
        self._current_ip = match.group(1) if match else None

    def set_ip(self, new_ip: str, subnet_mask: str = "255.255.255.0", gateway: str = "192.168.1.1") -> bool:
        """Set a new IP address for the interface."""
        if self.check_ip_availability(new_ip):
            print(f"IP address {new_ip} is already in use on the network.")
            return False

        command = f"netsh interface ip set address name=\"{self._interface_name}\" static {new_ip} {subnet_mask} {gateway}"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            self._current_ip = new_ip
            print(f"IP address changed successfully to {new_ip}.")
            return True
        else:
            print(f"Failed to change IP address: {result.stdout}")
            return False


@contextmanager
def redirect_output_to_file(file_path: str):
    """A context manager to redirect stdout and stderr to a file."""
    try:
        with open(file_path, 'a') as f:
            with redirect_stdout(f), redirect_stderr(f):
                yield
    finally:
        pass


def main() -> None:
    ip_manager = WindowsIPManager()
    if not ip_manager.is_admin():
        print("Not running as admin. Trying to elevate privileges.")
        ip_manager.run_as_admin()
    else:
        print(f"Running as an admin! Current IP Address: {ip_manager.current_ip}")
        if ip_manager.set_ip('192.168.1.37'):
            print(f"Updated IP Address: {ip_manager.current_ip}")


if __name__ == "__main__":
    with redirect_output_to_file('output.log'):
        main()
