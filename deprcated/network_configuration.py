
from network_utils import IPV4Address


import ctypes
import sys
import os
import subprocess
import re
from typing import Callable, List, Optional
from contextlib import contextmanager, redirect_stdout, redirect_stderr

from enums import AdapterType



class NetworkConfiguration:
    def __init__(self, _adapter_prefix, adapter_name: str, update_callback : Optional[Callable[..., None]] = None,) -> None:
        self._adapter_prefix     : str = _adapter_prefix
        self._adapter_name       : str = adapter_name
        self._ip_address         : IPV4Address = IPV4Address.from_string('0.0.0.0')
        self._subnet_mask        : IPV4Address = IPV4Address.from_string('255.255.255.255')
        self._default_gateway    : IPV4Address = IPV4Address.from_string('0.0.0.0')

        self.update_callback = update_callback

        self.request_network_configuration()

        if not IPV4Address.is_valid_subnet_mask(self._subnet_mask):
            raise ValueError("Invalid subnet mask: subnet masks must consist of consecutive ones followed by zeros.")

        if not self.is_gateway_in_same_network():
            raise ValueError("Default gateway must be in the same subnet as the IP address.")

    # ============================================================================================================

    @property
    def network_adapter(self) -> str:
        """Get the network adapter being used."""
        return self._adapter_name

    @network_adapter.setter
    def network_adapter(self, name: str) -> None:
        """Set the network adapter to be used."""
        print(f"Changing Network Adapter from {self._adapter_name} to {name}")
        self._adapter_name = name
        self.request_network_configuration()

    # ============================================================================================================

    @property
    def ip_address(self) -> IPV4Address:
        """Get the current IP address."""
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value: str) -> None:
        if not self.ip_available(value):
            self._ip_address = value
            print(f"IP address set to {value}")
        else:
            print(f"IP address {value} is already in use. No change applied.")

    # ============================================================================================================

    @property
    def subnet_mask(self):
        """Get the subnet mask of the network."""
        return self._subnet_mask

    @subnet_mask.setter
    def subnet_mask(self, value):
        """Set the subnet mask of the network."""
        self._subnet_mask = value

    # ============================================================================================================

    @property
    def default_gateway(self):
        """Get the network gateway address."""
        return self._default_gateway

    @default_gateway.setter
    def default_gateway(self, value):
        """Set the network gateway address."""
        self._default_gateway = value

    # ============================================================================================================

    def is_gateway_in_same_network(self) -> bool:
        ip_network = int.from_bytes(map(int, self._ip_address.octets), 'big')
        mask_network = int.from_bytes(map(int, self._subnet_mask.octets), 'big')
        gateway_network = int.from_bytes(map(int, self._default_gateway.octets), 'big')

        return (ip_network & mask_network) == (gateway_network & mask_network)

    @staticmethod
    def request_network_configuration(adapter_type, interface_name) -> None:
        """Update the current IP address from the system configuration."""
        prefix = 'Wireless LAN adapter' if adapter_type == AdapterType.WIFI else 'Ethernet adapter'

        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        pattern = rf"{prefix} {interface_name}.*?IPv4 Address[ .:]+([\d.]+)"
        match = re.search(pattern, result.stdout, re.S)
        ip = match.group(1) if match else None

    @staticmethod
    def commit_network_changes_as_admin(interface, ip, subnet, gateway):
        """
        Applies network settings with administrative privileges. This method changes the IP address,
        subnet mask, and default gateway for the specified network adapter using elevated privileges.

        Raises:
            PermissionError: If the method fails to gain elevated privileges.
            subprocess.CalledProcessError: If the network settings change fails.
        """
        # Locate the batch file relative to the current script
        bat_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quick_winip.bat'))

        # Prepare th
        # e arguments, ensuring they are correctly quoted to handle spaces and special characters
        args = f'"{interface}", "{ip}", "{subnet}", "{gateway}"'

        # Construct the PowerShell command
        ps_command = f'Powershell -Command "Start-Process \'{bat_file_path}\' -ArgumentList {args} -Verb RunAs"'

        # Execute the command
        try:
            subprocess.check_output(ps_command, shell=True)
            print("Network settings updated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e.output.decode()}")

    # ============================================================================================================

    @staticmethod
    def ip_available(ip: str) -> bool:
        """Check if the given IP address is in use on the network."""
        response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.DEVNULL)
        return response.returncode == 0

    # ============================================================================================================

    def __str__(self) -> str:
        prefix = 'Wireless LAN adapter' if self._adapter_type == AdapterType.WIFI else 'Ethernet adapter'
        return (f"Adapter Name: {self._adapter_name}\n"
                f"IP Address: {self._ip_address}\n"
                f"Subnet Mask: {self._subnet_mask}\n"
                f"Default Gateway: {self._default_gateway}")
