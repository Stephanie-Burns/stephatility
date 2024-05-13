
from typing import Pattern
import os
import re
import subprocess


from network_tools import AdapterType, IPV4Address, NetworkConfig


class IPV4AddressConfiguration:
    # Regular expressions to find IPv4 Address, Subnet Mask, and Default Gateway within the block
    _ipv4_regex     :Pattern[str] = re.compile(r"IPv4 Address[ .:]+([\d.]+)")
    _subnet_regex   :Pattern[str] = re.compile(r"Subnet Mask[ .:]+([\d.]+)")
    _gateway_regex  :Pattern[str] = re.compile(r"Default Gateway[ .:]+(?:.*?([\d.]+)\s*(?:%[\d]+)?\s*)+$", re.MULTILINE)

    @classmethod
    def get_configuration(cls, adapter_prefix: AdapterType, interface_name: str) -> NetworkConfig:
        prefix = 'Wireless LAN adapter' if adapter_prefix == AdapterType.WIFI else 'Ethernet adapter'

        # Regular expression to capture the relevant data block for the specified adapter
        capture_target_name = f'{prefix} {interface_name}'

        adapter_regex = re.compile(
            rf"{re.escape(capture_target_name)}:\s*\n(.*?)(?=\n\n|\Z)",
            re.DOTALL
        )

        # Find the relevant adapter block
        adapter_match = adapter_regex.search(cls.fetch_ipconfig_output())
        if not adapter_match:

            return NetworkConfig()

        adapter_block = adapter_match.group(1)

        # Extracting details
        ipv4_address = cls._ipv4_regex.search(adapter_block)
        subnet_mask = cls._subnet_regex.search(adapter_block)
        default_gateway = cls._gateway_regex.search(adapter_block)

        return NetworkConfig(
            adapter_prefix,
            interface_name,
            IPV4Address.from_string(ipv4_address.group(1) if ipv4_address else '0.0.0.0'),
            IPV4Address.from_string(subnet_mask.group(1) if subnet_mask else '255.255.255.0'),
            IPV4Address.from_string(default_gateway.group(1) if default_gateway else '0.0.0.0')
        )

    @staticmethod
    def fetch_ipconfig_output() -> str:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        return result.stdout

    @staticmethod
    def apply_configuration(config: NetworkConfig) -> None:
        """Throws exceptions if the interface cannot be configured."""
        bat_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quick_winip.bat'))
        args = f'"{config.adapter_name}", "{config.ipv4_address}", "{config.subnet_mask}", "{config.default_gateway}"'
        ps_command = f'Powershell -Command "Start-Process \'{bat_file_path}\' -ArgumentList {args} -Verb RunAs"'
        subprocess.check_output(ps_command, shell=True)


if __name__ == "__main__":
    ...
