
from dataclasses import dataclass, field
from typing import List, Iterable


@dataclass
class IPV4Address:
    octets: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate octets after dataclass is initialized."""
        self.validate_octets(self.octets)

    def __str__(self) -> str:
        """Return the string representation of the IPV4 address."""
        return ".".join(self.octets)

    def __getitem__(self, key: int) -> str:
        """Retrieve an octet by its index."""
        return self.octets[key]

    def __setitem__(self, key: int, value: str) -> None:
        """Set an octet at a specific index, validating the new value."""
        self.validate_octet(value)
        self.octets[key] = value

    def __len__(self) -> int:
        """Return the number of octets in the IPV4 address."""
        return len(self.octets)

    def __iter__(self) -> Iterable[str]:
        """Iterate over the octets of the IPV4 address."""
        return iter(self.octets)

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another IPV4Address instance or a string representation of an IP address.

        Args:
            other (object): Another IPV4Address instance or a string to compare.

        Returns:
            bool: True if both represent the same IP address, False otherwise.
        """
        if isinstance(other, IPV4Address):
            return self.octets == other.octets
        elif isinstance(other, str):
            try:
                other_ip = IPV4Address.from_string(other)
                return self.octets == other_ip.octets
            except ValueError:
                return False  # Invalid IP
        return NotImplemented

    def copy_from(self, other: 'IPV4Address') -> None:
        """
        Copies the octets from another IPV4Address instance, ensuring they are valid.

        Args:
            other (IPV4Address): The IPV4Address instance from which to copy octets.
        """
        self.octets = list(other.octets)
        self.validate_octets(self.octets)

    def is_valid_subnet_mask(self) -> bool:
        """
        Determines if the stored octets represent a valid subnet mask.

        Returns:
            bool: True if the subnet mask is valid, otherwise False.
        """
        bit_sequence = ''.join(f"{int(octet):08b}" for octet in self.octets)
        return '01' not in bit_sequence

    def update_from_string(self, ip_str: str) -> None:
        """
        Updates the IPV4Address's octets from a string representation.

        Args:
            ip_str (str): The string representation of an IPV4 address.
        """
        new_octets = ip_str.split('.')
        self.validate_octets(new_octets)
        self.octets = new_octets

    @classmethod
    def from_string(cls, ip_str: str) -> 'IPV4Address':
        """
        Create an IPV4Address instance from a string representation.

        Args:
            ip_str (str): The string representation of an IPV4 address.

        Returns:
            IPV4Address: A new instance of IPV4Address.
        """
        return cls(ip_str.split('.'))

    @classmethod
    def validate_octets(cls, octets: List[str]) -> None:
        """
        Validates a list of octets to ensure each is a valid IPV4 address component.

        Args:
            octets (List[str]): A list of string octets to validate.

        Raises:
            ValueError: If any octet is not a valid IPV4 address component.
        """
        if len(octets) != 4:
            raise ValueError("IP address must consist of exactly 4 octets.")
        for octet in octets:
            cls.validate_octet(octet)

    @staticmethod
    def validate_octet(octet: str) -> None:
        """
        Validates a single octet to ensure it is within the IPV4 address range.

        Args:
            octet (str): The octet to validate.

        Raises:
            ValueError: If the octet is not a valid number or not within the IPV4 address range.
        """
        try:
            octet_int = int(octet)
        except ValueError:
            raise ValueError(f"IP address octet '{octet}' must be an integer.")
        if not 0 <= octet_int <= 255:
            raise ValueError(f"IP address octet '{octet}' must be between 0 and 255.")

