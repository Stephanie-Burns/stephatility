
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPV4Address):
            return NotImplemented
        return self.octets == other.octets

    def copy_from(self, other: 'IPV4Address') -> None:
        """Copies octets from another IPV4Address instance."""
        self.octets = list(other.octets)  # Ensure a new list is created

        # Revalidate octets to ensure copied values are still valid
        self.validate_octets(self.octets)

    def is_valid_subnet_mask(self) -> bool:
        bit_sequence = ''.join(f"{int(octet):08b}" for octet in self.octets)
        return '01' not in bit_sequence

    @classmethod
    def from_string(cls, ip_str: str) -> 'IPV4Address':
        """Create an IPAddress instance from a string."""
        return cls(ip_str.split('.'))

    @classmethod
    def validate_octets(cls, octets: List[str]) -> None:
        if len(octets) != 4:
            raise ValueError("IP address must consist of exactly 4 octets.")
        for octet in octets:
            cls.validate_octet(octet)

    @staticmethod
    def validate_octet(octet: str) -> None:
        try:
            octet_int = int(octet)
        except ValueError:
            raise ValueError(f"IP address octet '{octet}' must be an integer.")
        if not 0 <= octet_int <= 255:
            raise ValueError(f"IP address octet '{octet}' must be between 0 and 255.")
