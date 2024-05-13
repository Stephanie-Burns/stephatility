
from typing import NamedTuple, Tuple

from network_tools.enums import AdapterType
from network_tools.network_config import NetworkConfig


class NetworkService:
    """
    Provides network configuration services, acting as a facade over underlying configuration management systems.

    Attributes:
        configuration_manager: An instance of a class that implements the configuration management logic for network settings.
    """
    def __init__(self, configuration_manager):
        self.configuration_manager = configuration_manager
        self.network_config = NetworkConfig()

    def get_network_configuration(
            self,
            adapter_type    : AdapterType = AdapterType.ETHERNET,
            interface_name  : str = 'Ethernet'
    ) -> NetworkConfig:
        """
        Retrieves the network configuration for a specific network adapter identified by type and name.

        Args:
            adapter_type (AdapterType): The type of the network adapter (e.g., WIFI, ETHERNET).
            interface_name (str): The name of the network interface.

        Returns:
            NamedTuple: An instance of NamedTuple containing network configuration details such as:
            IP address, subnet mask, and default gateway.

        Raises:
            Exception: Propagates exceptions that might be raised during the configuration fetching process.
        """

        backend_config_data = self.configuration_manager.get_configuration(adapter_type, interface_name)
        self.network_config.update_configuration(backend_config_data)

        return self.network_config

    def apply_configuration(self, config: NetworkConfig) -> Tuple[int, str]:
        """
        Applies a new network configuration to the specified interface.

        Args:
            config (NetworkConfig): The new network configuration settings to be applied.

        Returns:
            Tuple[int, str]: A tuple containing a status code (0 for success, 1 for failure) and a message describing the result.

        Raises:
            Exception: Captures and returns any exceptions as part of the error message in the tuple.
        """
        try:
            self.configuration_manager.apply_configuration(config)
            # app_config.save(config.as_dict())
            return 0, "Network settings updated successfully!"
        except Exception as e:
            return 1, str(e)

if __name__ == "__main__":
    # Example usage
    from ipv4_addrress_configuration import IPV4AddressConfiguration
    manager = IPV4AddressConfiguration()
    service = NetworkService(manager)
    service.get_network_configuration(AdapterType.ETHERNET, "Ethernet")
    service.get_network_configuration(AdapterType.WIFI, "Wi-Fi 2")
    service.apply_configuration("Ethernet", "192.168.1.37", "255.255.255.0", "192.168.1.1")



# service takes cinfig
# pings the adaptor name for signal, reads output, confirms that the change is indeed differnt,
# then it sets the ip

# Network should default to ehternet if it reads default config version
# ping adapter and if sucess fill data otherwise load default data in disabled set state
# user enters adapter name and pings for creds, sucess updates networkconfig, app config and gui
