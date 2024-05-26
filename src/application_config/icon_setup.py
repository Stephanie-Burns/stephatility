
from src.constants import ASSETS_DIR
from src.gui.icon_manager import IconManager


def initialize_icons():
    icon_manager = IconManager()
    icon_manager.register_icon('browse_folder', ASSETS_DIR / 'browse-folder-16.png')
    icon_manager.register_icon('live_folder', ASSETS_DIR / 'live-folder-16.png')
    icon_manager.register_icon('config', ASSETS_DIR / 'config-16.png')
    icon_manager.register_icon('file_extensions', ASSETS_DIR / 'file_extensions.png')
    icon_manager.register_icon('vault', ASSETS_DIR / 'vault-16.png')
    icon_manager.register_icon('item', ASSETS_DIR / 'item-16.png')

    return icon_manager
