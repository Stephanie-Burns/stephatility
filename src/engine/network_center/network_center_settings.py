
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from src.application_config.base.base_settings import BaseSettings
from src.engine.network_center.ipv4.network_config import NetworkConfig


def default_hosts() -> List[Tuple[str, str]]:
    return [
        ('', '')
    ]


def default_hosts_file() -> str:
    host_file_str = """\
    # Copyright (c) 1993-2009 Microsoft Corp.
    #
    # This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
    #
    # This file contains the mappings of IP addresses to host names. Each
    # entry should be kept on an individual line. The IP address should
    # be placed in the first column followed by the corresponding host name.
    # The IP address and the host name should be separated by at least one
    # space.
    #
    # Additionally, comments (such as these) may be inserted on individual
    # lines or following the machine name denoted by a '#' symbol.
    #
    # For example:
    #
    #      102.54.94.97     rhino.acme.com          # source server
    #       38.25.63.10     x.acme.com              # x client host

    # localhost name resolution is handle within DNS itself.
    #       127.0.0.1       localhost
    #       ::1             localhost
    """
    return host_file_str


def default_network_configuration() -> NetworkConfig:
    return NetworkConfig()


@dataclass
class NetworkCenterSettings(BaseSettings):
    hosts                   : List[Tuple[str, str]] = field(default_factory=default_hosts)
    last_seen_hosts_file    : str = field(default_factory=default_hosts_file)
    network_configuration   : NetworkConfig = field(default_factory=NetworkConfig)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "hosts": self.hosts,
            "last_seen_hosts_file": self.last_seen_hosts_file,
            "network_configuration": self.network_configuration.as_dict()
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'NetworkCenterSettings':
        return cls(
            hosts=config_dict.get("hosts", default_hosts()),
            last_seen_hosts_file=config_dict.get("last_seen_hosts_file", default_hosts_file()),
            network_configuration=NetworkConfig.from_dict(config_dict.get("network_configuration", {}))
        )

    def validate(self) -> bool:
        return True

    def get_network_configuration(self) -> NetworkConfig:
        return self.network_configuration if self.network_configuration else default_network_configuration()

    def set_network_configuration(self, network_config: NetworkConfig):
        if network_config is not self.network_configuration:
            raise Exception("Network configuration is already set.")
