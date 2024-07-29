
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Specific paths
ASSETS_DIR          = PROJECT_ROOT / 'assets' / 'icons'
LOGS_DIR            = PROJECT_ROOT / 'logs' / 'app.log'
USER_SETTINGS_JSON  = PROJECT_ROOT / 'user' / 'user_settings.json'
USER_SETTINGS_TOML  = PROJECT_ROOT / 'user' / 'user_settings.toml'  # TODO Deprecate
QUICK_WINIP_BAT     = PROJECT_ROOT / 'src' / 'engine' / 'network_center' / 'quick_winip.bat'
MODIFY_HOSTS_BAT    = PROJECT_ROOT / 'src' / 'engine' / 'network_center' / 'http_server' / 'modify_hosts.bat'


class Colors:
    HEART_POTION    = '#b373a8'
    ORBITAL         = '#7378b3'
    SAGE            = '#7eb373'
    BLACK           = '#000000'
    CARBON          = '#333333'
    MOON_BASE       = '#7b7b7b'
    CONCRETE        = '#d0d0d0'
    SNOWFLAKE       = '#f0f0f0'
    WHITE           = '#ffffff'
    LAKE_LUCERNE    = '#73a0b3'
    KIMONO          = '#7386b3'

    # =========================
    # Blue Grey
    BLUE_GRAY = '#7393B3'
    BLUE_GRAY_BRIGHT = '#e2e9f0'
    BLUE_GRAY_DARK = '#010101'
    BLUE_GRAY_DESATURATE = '#7e848a'

    # Adrift on the Nile
    ADRIFT = '#8eb6dd'
    ADRIFT_BRIGHT = '#d1e2f2'

    # Cavolo Nero
    CAVOLO_NERO = '#778DA4'
