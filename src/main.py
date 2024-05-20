
import tkinter as tk
from tkinter import PhotoImage

from src.application_config.logger import app_logger
from src.application_config.app_config import AppConfig
from src.engine.network_tools.http_server import ThreadManager
from src.engine.network_tools.http_server.local_file_server import LocalFileServer
from src.engine.network_tools import NetworkService
from src.engine.network_tools.ipv4 import IPV4AddressConfiguration
from src.gui import DirectoryCleaner, IPManager, ServeLocalFiles, TempFileGenerator


class StephaTility(tk.Frame):
    def __init__(self, parent: tk.Widget, app_config: AppConfig, **kwargs):
        super().__init__(parent, **kwargs)

        self.app_config = app_config

        self.network_service = NetworkService(IPV4AddressConfiguration(), self.app_config)
        self.network_service.get_network_configuration()

        self.thread_manager = ThreadManager()
        self.http_file_server = LocalFileServer(self.thread_manager)

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        # Initialize Containers
        self.directory_cleaner_0 = DirectoryCleaner(self, app_config.settings.directory_cleaners.dir0)
        self.directory_cleaner_0.grid(row=0, column=0,sticky=tk.EW, padx=5, pady=5)

        self.directory_cleaner_1 = DirectoryCleaner(self,app_config.settings.directory_cleaners.dir1)
        self.directory_cleaner_1.grid(row=1, column=0,sticky=tk.EW, padx=5, pady=5)

        self.tempfile_gen = TempFileGenerator(self, app_config.settings.tempfile_gen.extensions)
        self.tempfile_gen.grid(row=2, column=0,sticky=tk.EW, padx=5, pady=5)

        self.ip_manager = IPManager(self, self.network_service)
        self.ip_manager.grid(row=3, column=0, sticky=tk.EW, padx=5, pady=5)

        self.file_server = ServeLocalFiles(self, self.http_file_server, self.app_config.settings.http_file_server)
        self.file_server.grid(row=4, column=0, sticky=tk.EW, padx=5, pady=5)

    def on_close(self):
        """Handle the window close event to save the configuration before exiting."""
        self.app_config.save()
        self.thread_manager.stop_all_threads()
        self.master.destroy()


def main():

    app_logger.info("Starting GUI...")

    from pathlib import Path
    cfg = Path(__file__).resolve().parent / 'application_config' / 'settings.toml'
    app_config = AppConfig(settings_files=[str(cfg)])

    root = tk.Tk()
    root.title('StephaTility')

    icon_path = Path(__file__).resolve().parent.parent / 'assets' / 'icons' / "app.png"
    icon_image = PhotoImage(file=str(icon_path))
    root.iconphoto(False, icon_image)

    app = StephaTility(root, app_config)
    app.pack()

    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
