
from dataclasses import dataclass, field
from typing import List, Iterable


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



@dataclass
class NetworkConfiguration:
    adapter_name    : str
    ip_address      : IPV4Address
    subnet_mask     : IPV4Address
    default_gateway : IPV4Address

    def __post_init__(self):
        if not IPV4Address.is_valid_subnet_mask(self.subnet_mask):
            raise ValueError("Invalid subnet mask: subnet masks must consist of consecutive ones followed by zeros.")

        if not self.is_gateway_in_same_network():
            raise ValueError("Default gateway must be in the same subnet as the IP address.")

    def is_gateway_in_same_network(self) -> bool:
        ip_network = int.from_bytes(map(int, self.ip_address.octets), 'big')
        mask_network = int.from_bytes(map(int, self.subnet_mask.octets), 'big')
        gateway_network = int.from_bytes(map(int, self.default_gateway.octets), 'big')

        return (ip_network & mask_network) == (gateway_network & mask_network)

    def __str__(self) -> str:
        return (f"Adapter Name: {self.adapter_name}\n"
                f"IP Address: {self.ip_address}\n"
                f"Subnet Mask: {self.subnet_mask}\n"
                f"Default Gateway: {self.default_gateway}")


if __name__ == '__main__':

    # IPV4Address - Example Usage
    ip1 = IPV4Address.from_string("192.168.1.1")
    ip2 = IPV4Address(['192', '168', '1', '1'])

    print(ip1)  # Output: 192.168.1.1
    print(ip2)  # Output: 192.168.1.1

    ip1[0] = '10'
    print(ip1)  # Output: 10.168.1.1

    for octet_value in ip1:
        print(octet_value)


    # NetworkConfiguration - Example Usage
    try:
        ip_address = IPV4Address.from_string("192.168.1.100")
        subnet_mask = IPV4Address.from_string("255.255.255.0")
        default_gateway = IPV4Address.from_string("192.168.1.1")

        network_config = NetworkConfiguration(
            adapter_name="Ethernet",
            ip_address=ip_address,
            subnet_mask=subnet_mask,
            default_gateway=default_gateway
        )

        print(network_config)
    except ValueError as e:
        print(e)
