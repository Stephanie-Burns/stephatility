
from typing import NamedTuple, Tuple

from enums import AdapterType


class NetworkService:
    """
    Provides network configuration services, acting as a facade over underlying configuration management systems.

    Attributes:
        configuration_manager: An instance of a class that implements the configuration management logic for network settings.
    """
    def __init__(self, configuration_manager):
        self.configuration_manager = configuration_manager

    def get_network_configuration(self, adapter_type: AdapterType, interface_name) -> NamedTuple:
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
        return self.configuration_manager.get_configuration(adapter_type, interface_name)

    def apply_changes(self, interface: str, ip: str, subnet: str, gateway: str) -> Tuple[int, str]:
        """
        Applies new network configuration settings to a specified interface.

        Args:
            interface (str): The name of the interface where settings will be applied.
            ip (str): The new IP address to set.
            subnet (str): The new subnet mask.
            gateway (str): The new default gateway.

        Returns:
            Tuple[int, str]: A tuple containing a status code (0 for success, 1 for failure) and a message describing the result.

        Raises:
            Exception: Captures and returns any exceptions as part of the error message in the tuple.
        """
        try:
            self.configuration_manager.apply_configuration(interface, ip, subnet, gateway)
            return 0, "Network settings updated successfully!"

        except Exception as e:
            return 1, str(e)

if __name__ == "__main__":
    # Example usage
    from ipv4_network_management import IPV4AddressConfiguration
    manager = IPV4AddressConfiguration()
    service = NetworkService(manager)
    service.get_network_configuration(AdapterType.ETHERNET, "Ethernet")
    service.get_network_configuration(AdapterType.WIFI, "Wi-Fi 2")
    service.apply_changes("Ethernet", "192.168.1.37", "255.255.255.0", "192.168.1.1")
