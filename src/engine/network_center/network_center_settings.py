
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from src.application_config.base.base_settings import BaseSettings


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


def default_network_configuration() -> Dict[str, str]:
    return {
        "default_gateway"   : "0.0.0.0",
        "subnet_mask"       : "255.255.255.0",
        "ipv4_address"      : "192.168.1.37",
        "adapter_name"      : "Ethernet",
        "adapter_prefix"    : "ethernet",
}


@dataclass
class NetworkCenterSettings(BaseSettings):
    hosts                   : List[Tuple[str, str]] = field(default_factory=default_hosts)
    last_seen_hosts_file    : str = field(default_factory=default_hosts_file)
    network_configuration   : dict = field(default_factory=default_network_configuration)

    def validate(self) -> bool:
        return True
