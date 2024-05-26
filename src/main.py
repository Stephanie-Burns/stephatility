import tkinter as tk
from tkinter import PhotoImage

from src.constants import ASSETS_DIR, SETTINGS_TOML, USER_SETTINGS_JSON
from src.application_config.app_logger import app_logger
from src.application_config.app_config import AppConfig
from src.application_config.user_settings import UserSettings
from src.engine.network_center.http_server import ThreadManager
from src.gui.containers.file_center import FileCenter
from src.gui.containers.network_center import NetworkCenter
from src.gui.styles import configure_styles
from src.application_config.icon_setup import initialize_icons



class StephaTility(tk.Frame):
    def __init__(self, parent: tk.Widget, app_config: AppConfig, user_settings: UserSettings, **kwargs):
        super().__init__(parent, **kwargs)

        self.app_config = app_config
        self.user_settings = user_settings
        self.thread_manager = ThreadManager()

        configure_styles()
        initialize_icons()

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Initialize Containers
        self.file_center = FileCenter(self, self.user_settings.file_center)
        self.file_center.grid(row=0, column=0, columnspan=5, sticky=tk.EW, padx=5, pady=5)

        self.network_center = NetworkCenter(
            self,
            self.app_config,
            self.thread_manager
        )
        self.network_center.grid(row=1, column=0, columnspan=5, sticky=tk.EW, padx=5, pady=5)

    def on_close(self):
        """Handle the window close event to save the configuration before exiting."""
        self.app_config.save()
        self.user_settings.save_settings()
        self.thread_manager.stop_all_threads()
        self.master.destroy()


def main():
    app_logger.info("Starting GUI...")

    app_config = AppConfig(settings_files=[str(SETTINGS_TOML)])
    user_settings = UserSettings(USER_SETTINGS_JSON)

    root = tk.Tk()
    root.title('StephaTility')

    icon_path = ASSETS_DIR / "app.png"
    icon_image = PhotoImage(file=str(icon_path))
    root.iconphoto(False, icon_image)

    app = StephaTility(root, app_config, user_settings)
    app.pack(fill='both', expand=True)

    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
