
from typing import NamedTuple, Optional, Tuple

from src.network_tools import NetworkConfig


class NetworkService:
    """
    Provides network configuration services, acting as a facade over underlying configuration management systems.

    Attributes:
        configuration_strategy: An instance of a class that implements the configuration management logic for network settings.
    """
    def __init__(self, configuration_strategy, application_config: Optional['AppConfig'] = None):
        self.configuration_strategy = configuration_strategy
        self.app_config = application_config
        self.network_config = self.app_config.get_network_config()

    def get_network_configuration(self) -> NetworkConfig:
        """
        Retrieves the network configuration for a specific network adapter identified by type and name.

        Returns:
            NamedTuple: An instance of NamedTuple containing network configuration details such as:
            IP address, subnet mask, and default gateway.

        Raises:
            Exception: Propagates exceptions that might be raised during the configuration fetching process.
        """

        self.network_config.update_configuration(self.network_config)

        return self.network_config

    def apply_configuration(self) -> Tuple[int, str]:
        """
        Applies a new network configuration to the specified interface.

        Returns:
            Tuple[int, str]: A tuple containing a status code (0 for success, 1 for failure) and a message describing the result.

        Raises:
            Exception: Captures and returns any exceptions as part of the error message in the tuple.
        """
        try:
            self.configuration_strategy.apply_configuration(self.network_config)

            if self.app_config:
                self.app_config.set_network_config(self.network_config)
                self.app_config.save()

            return 0, "Network settings updated successfully!"

        except Exception as e:
            return 1, str(e)


if __name__ == "__main__":

    # Example usage
    from ipv4_addrress_configuration import IPV4AddressConfiguration
    manager = IPV4AddressConfiguration()
    service = NetworkService(manager)

    service.network_config.ipv4_address.update_from_string("192.168.1.37")
    service.apply_configuration()
    service.get_network_configuration()
