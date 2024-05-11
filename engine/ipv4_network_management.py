
from typing import NamedTuple, Pattern
import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import List, Iterable

from deprcated.network_utils import IPV4Address
from enums import AdapterType


@dataclass
class IPV4Address:
    octets: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.validate_octets(self.octets)

    def __str__(self) -> str:
        return ".".join(self.octets)

    def __getitem__(self, key: int) -> str:
        return self.octets[key]

    def __setitem__(self, key: int, value: str) -> None:
        self.validate_octet(value)
        self.octets[key] = value

    def __len__(self) -> int:
        return len(self.octets)

    def __iter__(self) -> Iterable[str]:
        return iter(self.octets)

    @staticmethod
    def validate_octet(octet: str) -> None:
        if not 0 <= int(octet) <= 255:
            raise ValueError(f"IP address octet {octet} must be between 0 and 255.")

    @classmethod
    def validate_octets(cls, octets: List[str]) -> None:
        for octet in octets:
            cls.validate_octet(octet)  # Reuse validation logic for consistency

    @classmethod
    def from_string(cls, ip_str: str) -> 'IPV4Address':
        """Create an IPAddress instance from a string."""
        return cls(ip_str.split('.'))

    @staticmethod
    def is_valid_subnet_mask(mask: 'IPV4Address') -> bool:
        # Convert to a single string of bits
        bit_sequence = ''.join(f"{int(octet):08b}" for octet in mask.octets)
        # Check if the bit sequence is a valid mask (ones followed by zeros)
        if '01' in bit_sequence:
            return False
        return True


class NetworkConfig(NamedTuple):
    adapter_prefix  : AdapterType
    adapter_name    : str
    ipv4_address    : IPV4Address
    subnet_mask     : IPV4Address
    default_gateway : IPV4Address


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

            return NetworkConfig(adapter_prefix, interface_name, IPV4Address.from_string('0.0.0.0'), IPV4Address.from_string('255.255.255.255'), IPV4Address.from_string('0.0.0.0'))

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
    def apply_configuration(interface: str, ip: str, subnet: str, gateway: str) -> None:
        """Throws exceptions if the interface cannot be configured."""
        bat_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quick_winip.bat'))
        args = f'"{interface}", "{ip}", "{subnet}", "{gateway}"'
        ps_command = f'Powershell -Command "Start-Process \'{bat_file_path}\' -ArgumentList {args} -Verb RunAs"'
        subprocess.check_output(ps_command, shell=True)


if __name__ == "__main__":
    ...
