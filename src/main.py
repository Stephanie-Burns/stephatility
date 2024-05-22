
import tkinter as tk
from tkinter import PhotoImage

from src.constants import ASSETS_DIR, SETTINGS_TOML
from src.application_config.logger import app_logger
from src.application_config.app_config import AppConfig
from src.engine.network_tools.http_server import ThreadManager
from src.engine.network_tools.http_server.local_file_server import LocalFileServer
from src.engine.network_tools import NetworkService
from src.engine.network_tools.ipv4 import IPV4AddressConfiguration
from src.gui import DirectoryCleaner, IPManager, ServeLocalFiles, TempFileGenerator
from src.gui.containers.network_center import NetworkCenter


class StephaTility(tk.Frame):
    def __init__(self, parent: tk.Widget, app_config: AppConfig, **kwargs):
        super().__init__(parent, **kwargs)

        self.app_config = app_config
        self.thread_manager = ThreadManager()

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        # Initialize Containers
        self.directory_cleaner_0 = DirectoryCleaner(self, app_config.settings.directory_cleaners.dir0)
        self.directory_cleaner_0.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)

        self.directory_cleaner_1 = DirectoryCleaner(self, app_config.settings.directory_cleaners.dir1)
        self.directory_cleaner_1.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)

        self.tempfile_gen = TempFileGenerator(self, app_config.settings.tempfile_gen.extensions)
        self.tempfile_gen.grid(row=2, column=0, sticky=tk.EW, padx=5, pady=5)

        self.network_center = NetworkCenter(
            self,
            self.app_config,
            self.thread_manager
        )
        self.network_center.grid(row=3, column=0, sticky=tk.EW, padx=5, pady=5)


    def on_close(self):
        """Handle the window close event to save the configuration before exiting."""
        self.app_config.save()
        self.thread_manager.stop_all_threads()
        self.master.destroy()


def main():

    app_logger.info("Starting GUI...")

    app_config = AppConfig(settings_files=[str(SETTINGS_TOML)])

    root = tk.Tk()
    root.title('StephaTility')

    icon_path = ASSETS_DIR / "app.png"
    icon_image = PhotoImage(file=str(icon_path))
    root.iconphoto(False, icon_image)

    app = StephaTility(root, app_config)
    app.pack()

    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
