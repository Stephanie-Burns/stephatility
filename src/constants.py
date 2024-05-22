
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Specific paths
ASSETS_DIR          = PROJECT_ROOT / 'assets' / 'icons'
LOGS_DIR            = PROJECT_ROOT / 'logs' / 'app.log'
SETTINGS_TOML       = PROJECT_ROOT / 'src' / 'application_config' / 'settings.toml'  # TODO Deprecate
USER_SETTINGS_JSON  = PROJECT_ROOT / 'src' / 'application_config' / 'user_settings.json'
USER_SETTINGS_TOML  = PROJECT_ROOT / 'user' / 'user_settings.toml'  # TODO Deprecate
QUICK_WINIP_BAT     = PROJECT_ROOT / 'src' / 'engine' / 'network_tools' / 'quick_winip.bat'
MODIFY_HOSTS_BAT    = PROJECT_ROOT / 'src' / 'engine' / 'network_tools' / 'http_server' / 'modify_hosts.bat'


class Colors:
    ORBITAL = "#7378b3"
    BLUE_GRAY = "#7393B3"
    HEART_POTION = "#b373a8"
    SAGE = "#7eb373"
    WHITE = "#ffffff"
    CARBON = "#333333"
    SNOWFLAKE = '#f0f0f0'  # soft white
    CONCRETE = '#d0d0d0'
