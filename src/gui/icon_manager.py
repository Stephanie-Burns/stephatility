import tkinter as tk
from pathlib import Path
from typing import Dict, Tuple

from src.application_config.app_logger import app_logger


class IconManager:
    """
    IconManager is a Singleton class responsible for loading, resizing, and caching icons in a Tkinter application.

    This class ensures that icons are only loaded once and cached for future use, improving the performance and efficiency
    of the application. It also handles missing icons gracefully by returning a default icon when an icon is not found or
    cannot be loaded.

    Usage:
        # Initialize the IconManager (only once, Singleton)
        icon_manager = IconManager()

        # Register icons with their respective paths
        icon_manager.register_icon('browse_folder', Path('path/to/browse-folder-16.png'))
        icon_manager.register_icon('live_folder', Path('path/to/live-folder-16.png'))

        # Retrieve icons as needed
        browse_icon = icon_manager.get_icon('browse_folder', (16, 16))
        live_icon = icon_manager.get_icon('live_folder', (32, 32))
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            app_logger.debug("Created new singleton instance:%s", cls.__name__)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Ensure this runs only once
            self._loaded_icons  : Dict[Tuple[str, Tuple[int, int]], tk.PhotoImage] = {}
            self._icon_paths    : Dict[str, Path] = {}
            self._initialized   : bool = True

            self.default_icon   : tk.PhotoImage = self._create_default_icon()

    def register_icon(self, icon_name: str, icon_path: Path) -> None:
        """
        Registers an icon with a given name and path.

        Args:
            icon_name (str): The name to register the icon under.
            icon_path (Path): The file path to the icon image.
        """
        self._icon_paths[icon_name] = icon_path

    def get_icon(self, icon_name: str, icon_size: Tuple[int, int]) -> tk.PhotoImage:
        """
        Retrieves a cached icon, resizing it if necessary. If the icon is not found, a default icon is returned.

        Args:
            icon_name (str): The name of the icon to retrieve.
            icon_size (Tuple[int, int]): The desired size of the icon (width, height).

        Returns:
            tk.PhotoImage: The requested icon or a default icon if the requested icon is not found.
        """
        key = (icon_name, icon_size)

        if key in self._loaded_icons:
            app_logger.debug("Loaded cached icon '%s' with size %s.", icon_name, icon_size)
            return self._loaded_icons[key]

        icon_path = self._icon_paths.get(icon_name)

        if not icon_path:
            app_logger.warning("Icon '%s' not found. Using default icon.", icon_name)
            return self.default_icon

        return self._load_and_cache_icon(icon_name, icon_path, icon_size, key)

    def _load_and_cache_icon(
            self,
            icon_name   : str,
            icon_path   : Path,
            icon_size   : Tuple[int, int],
            key         : Tuple[str, Tuple[int, int]]
    ) -> tk.PhotoImage:
        """
        Loads and caches an icon from the given path.

        Args:
            icon_name (str): The name of the icon to retrieve.
            icon_path (Path): The file path to the icon image.
            icon_size (Tuple[int, int]): The desired size of the icon (width, height).
            key (Tuple[str, Tuple[int, int]]): The key to use for caching the icon.

        Returns:
            tk.PhotoImage: The loaded and resized icon or a default icon if loading fails.
        """
        try:
            icon = tk.PhotoImage(file=str(icon_path))
            resized_icon = self._resize_icon(icon, icon_size)
            self._loaded_icons[key] = resized_icon

            app_logger.debug("Cached icon '%s' with size %s.", icon_name, icon_size)
            return resized_icon

        except Exception as e:
            app_logger.error("Error loading icon '%s': %s. Using default icon.", icon_name, e)
            return self.default_icon

    @staticmethod
    def _resize_icon(icon: tk.PhotoImage, icon_size: Tuple[int, int]) -> tk.PhotoImage:
        """
        Resizes an icon to the specified size.

        Args:
            icon (tk.PhotoImage): The original icon to resize.
            icon_size (Tuple[int, int]): The desired size of the icon (width, height).

        Returns:
            tk.PhotoImage: The resized icon.
        """
        return icon.subsample(
            max(icon.width() // icon_size[0], 1),
            max(icon.height() // icon_size[1], 1)
        )

    @staticmethod
    def _create_default_icon() -> tk.PhotoImage:
        """
        Creates a default placeholder icon.

        Returns:
            tk.PhotoImage: A default placeholder icon.
        """
        default_icon = tk.PhotoImage(width=16, height=16)
        default_icon.put("gray", to=(0, 0, 16, 16))
        return default_icon
