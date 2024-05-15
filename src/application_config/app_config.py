
from typing import List, Optional

import toml
from dynaconf import Dynaconf

from src.application_config.logger import app_logger
from src.network_tools import NetworkConfig, AdapterType


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class AppConfig:
    def __init__(self, settings_files: Optional[List[str]] = None):
        if settings_files is None:
            settings_files = ['settings.toml']

        self.settings_files = settings_files
        self.settings = Dynaconf(settings_files=self.settings_files)

        app_logger.debug(f"Initialized configuration with files: {self.settings_files}")

    def get_network_config(self) -> NetworkConfig:
        config_dict = {
            "adapter_prefix": AdapterType(self.settings.network.adapter_prefix),
            "adapter_name": self.settings.network.adapter_name,
            "ipv4_address": self.settings.network.ipv4_address,
            "subnet_mask": self.settings.network.subnet_mask,
            "default_gateway": self.settings.network.default_gateway
        }
        return NetworkConfig.from_dict(config_dict)

    def set_network_config(self, config: NetworkConfig) -> None:
        self.settings.set("network.adapter_prefix", config.adapter_prefix.value)
        self.settings.set("network.adapter_name", config.adapter_name)
        self.settings.set("network.ipv4_address", str(config.ipv4_address))
        self.settings.set("network.subnet_mask", str(config.subnet_mask))
        self.settings.set("network.default_gateway", str(config.default_gateway))

        app_logger.debug("Updated network configuration: %s", config.to_dict())

    def save(self) -> None:
        for settings_file in self.settings_files:
            try:
                with open(settings_file, 'w') as f:
                    toml.dump(self.settings.as_dict(), f)

                    app_logger.debug("Saved configuration to file: %s", settings_file)

            except Exception as e:
                app_logger.error("Error saving configuration to file: %s", settings_file)
                raise ConfigError(f"Error saving configuration to file: {settings_file}") from e


# if __name__ == '__main__':
#     # Initialize the configuration
#     config = AppConfig()
#
#     # Access configuration values using the methods
#     my_adapter_prefix = config.get_network_adapter_prefix()
#     my_adapter_name = config.get_network_adapter_name()
#
#     print(f"Adapter Prefix: {my_adapter_prefix}")
#     print(f"Adapter Name: {my_adapter_name}")
#
#     # Change the adapter type and save it back to the configuration
#     config.set_network_adapter_prefix(AdapterType.WIFI)
#     config.save()
#
#     # Verify the change
#     new_adapter_prefix = config.get_network_adapter_prefix()
#     print(f"New Adapter Prefix: {new_adapter_prefix}")
