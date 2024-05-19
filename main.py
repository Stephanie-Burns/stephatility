
import tkinter as tk

from src.application_config.logger import app_logger
from src.application_config.app_config import AppConfig
from src.gui import DirectoryCleaner, IPManager, ServeLocalFiles, TempFileGenerator
from src.network_tools import IPV4AddressConfiguration, NetworkService


import threading
import logging

class ThreadService:
    def __init__(self):
        self.threads = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def add_thread(self, thread):
        with self.lock:
            self.threads.append(thread)
            thread.start()

    def stop_all_threads(self):
        self.stop_event.set()
        with self.lock:
            for thread in self.threads:
                if thread.is_alive():
                    thread.join()
            self.threads = []
        self.stop_event.clear()

    def remove_thread(self, thread):
        with self.lock:
            if thread in self.threads:
                self.threads.remove(thread)



class UtilApp(tk.Frame):
    def __init__(self, parent: tk.Widget, app_config: AppConfig, **kwargs):
        super().__init__(parent, **kwargs)

        self.app_config = app_config
        self.network_service = NetworkService(IPV4AddressConfiguration(), self.app_config)
        self.network_service.get_network_configuration()
        self.thread_service = ThreadService()

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

        self.local_file_server = ServeLocalFiles(self, self.thread_service)
        self.local_file_server.grid(row=4, column=0, sticky=tk.EW, padx=5, pady=5)

    def on_close(self):
        """Handle the window close event to save the configuration before exiting."""
        self.app_config.save()
        self.thread_service.stop_all_threads()
        self.master.destroy()


def main():

    app_logger.info("Starting GUI...")
    from pathlib import Path
    cfg = Path(__file__).resolve().parent / 'src' / 'application_config' / 'settings.toml'
    app_config = AppConfig(settings_files=[cfg])

    root = tk.Tk()
    root.title('StephAtility (lol)')
    app = UtilApp(root, app_config)
    app.pack()

    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
