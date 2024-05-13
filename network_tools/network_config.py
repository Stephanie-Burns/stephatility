
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Union

from network_tools.enums import AdapterType
from network_tools.ipv4_address import IPV4Address


@dataclass
class NetworkConfig:
    adapter_prefix  : AdapterType = AdapterType.ETHERNET
    adapter_name    : str = 'Ethernet'
    ipv4_address    : IPV4Address = field(default_factory=lambda: IPV4Address.from_string('0.0.0.0'))
    subnet_mask     : IPV4Address = field(default_factory=lambda: IPV4Address.from_string('255.255.255.0'))
    default_gateway : IPV4Address = field(default_factory=lambda: IPV4Address.from_string('0.0.0.0'))
    previous_config : Dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        """Post-initialization to validate and capture the initial configuration."""
        self._validate_network_config()
        self._capture_initial_config()

    def __eq__(self, other: object) -> bool:
        """Check equality by comparing configurations."""
        if not isinstance(other, NetworkConfig):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def _validate_network_config(self) -> None:
        """Validate that all configuration fields are instances of IPV4Address."""
        if not all(isinstance(i, IPV4Address) for i in [self.ipv4_address, self.subnet_mask, self.default_gateway]):
            raise ValueError("All IP-related fields must be instances of IPV4Address.")

    def _capture_initial_config(self) -> None:
        """Capture the initial state of the configuration for change tracking."""
        self.previous_config = self.to_dict()

    def has_changed(self) -> bool:
        """Determine if the current configuration has changed from the previously captured state."""
        return self.to_dict() != self.previous_config

    def reset_baseline(self) -> None:
        """Reset the baseline configuration to the current state."""
        self._capture_initial_config()

    def update_configuration(self, new_config: Union['NetworkConfig', Dict[str, Any]]) -> None:
        """Update the configuration using another NetworkConfig object or a dictionary.

        Args:
            new_config (Union[NetworkConfig, Dict[str, Any]]): The new configuration to apply.

        Raises:
            ValueError: If new_config is neither a NetworkConfig object nor a valid dictionary.
        """
        if isinstance(new_config, dict):
            for key, value in new_config.items():
                if hasattr(self, key) and isinstance(value, type(getattr(self, key))):
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid type for {key} or {key} is not a valid attribute of NetworkConfig")
        elif isinstance(new_config, NetworkConfig):
            self.adapter_prefix = new_config.adapter_prefix
            self.adapter_name = new_config.adapter_name
            self.ipv4_address = new_config.ipv4_address
            self.subnet_mask = new_config.subnet_mask
            self.default_gateway = new_config.default_gateway
        else:
            raise ValueError("new_config must be either a NetworkConfig instance or a dictionary")

        self._validate_network_config()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the current configuration to a dictionary."""
        return {
            "adapter_prefix": self.adapter_prefix,
            "adapter_name": self.adapter_name,
            "ipv4_address": str(self.ipv4_address),
            "subnet_mask": str(self.subnet_mask),
            "default_gateway": str(self.default_gateway)
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'NetworkConfig':
        """Create a NetworkConfig instance from a dictionary.

        Args:
            config_dict (Dict[str, Any]): A dictionary containing all necessary configuration keys.

        Returns:
            NetworkConfig: A new instance of NetworkConfig configured as per the dictionary.
        """
        return cls(
            adapter_prefix=AdapterType[config_dict['adapter_prefix']],
            adapter_name=config_dict['adapter_name'],
            ipv4_address=IPV4Address.from_string(config_dict['ipv4_address']),
            subnet_mask=IPV4Address.from_string(config_dict['subnet_mask']),
            default_gateway=IPV4Address.from_string(config_dict['default_gateway'])
        )

    def clone(self) -> 'NetworkConfig':
        """Create a deep copy of the current configuration.

        Returns:
            NetworkConfig: A new instance of NetworkConfig that is a deep copy of this configuration.
        """
        return deepcopy(self)


if __name__ == '__main__':

    # Create initial configuration
    initial_ip = IPV4Address(["192", "168", "1", "100"])
    subnet = IPV4Address(["255", "255", "255", "0"])
    gateway = IPV4Address(["192", "168", "1", "1"])

    config = NetworkConfig(AdapterType.ETHERNET, "eth0", initial_ip, subnet, gateway)
    print("Initial Configuration:", config)
    print("Has configuration changed from baseline?", config.has_changed())

    # Change the IP and update configuration
    new_ip = IPV4Address(["192", "168", "1", "101"])
    config.update_configuration({'ipv4_address': new_ip})
    print("Updated Configuration:", config)

    # Check if changes have been applied
    print("Has configuration changed from baseline?", config.has_changed())

    # Reset the baseline to current configuration
    config.reset_baseline()
    print("Reset baseline, check again:", config.has_changed())

    # Clone the configuration
    clone_config = config.clone()
    print("Cloned Configuration:", clone_config)

    # Verify equality
    print("Is cloned config same as original?", clone_config is config)
