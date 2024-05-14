
import os
import re
import subprocess
from typing import Optional, Pattern

from network_tools.enums import AdapterType
from network_tools.network_config import NetworkConfig


class IPV4AddressConfiguration:
    # Regular expressions to find IPv4 Address, Subnet Mask, and Default Gateway within the block
    _ipv4_regex     :Pattern[str] = re.compile(r"IPv4 Address[ .:]+([\d.]+)")
    _subnet_regex   :Pattern[str] = re.compile(r"Subnet Mask[ .:]+([\d.]+)")
    _gateway_regex  :Pattern[str] = re.compile(r"Default Gateway[ .:]+(?:.*?([\d.]+)\s*(?:%[\d]+)?\s*)+$", re.MULTILINE)


    @staticmethod
    def apply_configuration(config: NetworkConfig) -> None:
        """
        Applies the given network configuration using a system command, potentially requiring elevated privileges.

        Args:
            config (NetworkConfig): The configuration to apply.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        bat_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quick_winip.bat'))
        args = f'"{config.adapter_name}", "{config.ipv4_address}", "{config.subnet_mask}", "{config.default_gateway}"'
        ps_command = f'Powershell -Command "Start-Process \'{bat_file_path}\' -ArgumentList {args} -Verb RunAs"'
        subprocess.check_output(ps_command, shell=True)

    @classmethod
    def get_configuration(cls, network_config: NetworkConfig) -> None:
        """
        Retrieves and updates the network configuration for a specified network adapter.

        Args:
            network_config (NetworkConfig): The network configuration object to update.

        Raises:
            ValueError: If no configuration data is found for the adapter.
        """
        adapter_block = cls.fetch_adapter_block(network_config.adapter_name)
        if not adapter_block:
            raise ValueError(f"No data found for adapter {network_config.adapter_name}")
        cls.extract_ip_details(adapter_block, network_config)

    @classmethod
    def extract_ip_details(cls, adapter_block: str, network_config: NetworkConfig) -> None:
        """
        Extracts and updates the network configuration object with IP address, subnet mask, and gateway details from the adapter block.

        Args:
            adapter_block (str): The text block containing IP configuration details.
            network_config (NetworkConfig): The network configuration object to be updated.
        """
        ipv4_address    = cls._ipv4_regex.search(adapter_block)
        subnet_mask     = cls._subnet_regex.search(adapter_block)
        default_gateway = cls._gateway_regex.search(adapter_block)

        if ipv4_address:
            network_config.ipv4_address.update_from_string(ipv4_address.group(1))
        if subnet_mask:
            network_config.subnet_mask.update_from_string(subnet_mask.group(1))
        if default_gateway:
            network_config.default_gateway.update_from_string(default_gateway.group(1))

    @classmethod
    def fetch_adapter_block(cls, adapter_name: str) -> Optional[str]:
        """
        Fetches the network configuration block from the system's IP configuration output for a specific adapter.

        Args:
            adapter_name (str): The name of the network adapter.

        Returns:
            Optional[str]: The configuration block as a string if found, otherwise None.
        """
        prefix = 'Wireless LAN adapter' if adapter_name == AdapterType.WIFI else 'Ethernet adapter'
        adapter_regex = re.compile(
            rf"{re.escape(prefix + ' ' + adapter_name)}:\s*\n(.*?)(?=\n\n|\Z)",
            re.DOTALL
        )
        output = cls.fetch_ipconfig_output()
        match = adapter_regex.search(output)
        return match.group(1) if match else None

    @staticmethod
    def fetch_ipconfig_output() -> str:
        """
        Fetches the system's IP configuration output via the 'ipconfig' command.

        Returns:
            str: The output from the 'ipconfig' command.
        """
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        return result.stdout







if __name__ == "__main__":
    ...
