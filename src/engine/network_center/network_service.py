
import platform
from typing import NamedTuple, Optional, Tuple

from src.engine.network_center.ipv4 import  NetworkConfig
from src.engine.network_center.network_center_settings import NetworkCenterSettings


class NetworkService:
    """
    Provides network configuration services, acting as a facade over underlying configuration management systems.

    Attributes:
        configuration_strategy: An instance of a class that implements the configuration management logic for network settings.
    """
    def __init__(self, configuration_strategy, user_settings: NetworkCenterSettings = None):
        self.configuration_strategy = configuration_strategy
        self.user_settings = user_settings
        self.network_config = self.user_settings.get_network_configuration()

    def get_network_configuration(self) -> NetworkConfig:
        """
        Retrieves the network configuration for a specific network adapter identified by type and name.

        Returns:
            NamedTuple: An instance of NamedTuple containing network configuration details such as:
            IP address, subnet mask, and default gateway.

        Raises:
            Exception: Propagates exceptions that might be raised during the configuration fetching process.
        """

        # Neutered for Linux testing, it needs to be a strategy oneday. :)
        if platform.system() == 'Windows':
            self.configuration_strategy.get_configuration(self.network_config)

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

            if self.user_settings:
                self.user_settings.set_network_configuration(self.network_config)

            return 0, "Network settings updated successfully!"

        except Exception as e:
            return 1, str(e)


if __name__ == "__main__":

    # Example usage
    from src.engine.network_center.ipv4.ipv4_addrress_configuration import IPV4AddressConfiguration
    manager = IPV4AddressConfiguration()
    service = NetworkService(manager)

    service.network_config.ipv4_address.update_from_string("192.168.1.37")
    service.apply_configuration()
    service.get_network_configuration()
