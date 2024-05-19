
import tkinter as tk

from src.application_config.logger import app_logger
from src.application_config.app_config import AppConfig
from src.gui import DirectoryCleaner, IPManager, ServeLocalFiles, TempFileGenerator
from src.network_tools import IPV4AddressConfiguration, NetworkService


import threading
from typing import Callable


class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.locks = {}
        self.stop_events = {}
        self.lock = threading.Lock()

    def add_thread(self, target: Callable, args: tuple, daemon: bool = True) -> int:
        stop_event = threading.Event()
        thread = threading.Thread(target=target, args=args + (stop_event,))
        thread.daemon = daemon
        with self.lock:
            thread.start()
            self.threads[thread.ident] = thread
            self.locks[thread.ident] = threading.Lock()
            self.stop_events[thread.ident] = stop_event
            return thread.ident

    def stop_thread(self, identifier: int):
        with self.lock:
            stop_event = self.stop_events.pop(identifier, None)
            thread = self.threads.pop(identifier, None)
            if stop_event and thread:
                stop_event.set()
                thread.join()
                self.locks.pop(identifier, None)

    def stop_all_threads(self):
        with self.lock:
            for identifier, thread in list(self.threads.items()):
                stop_event = self.stop_events.pop(identifier, None)
                if stop_event:
                    stop_event.set()
                if thread.is_alive():
                    thread.join()
            self.threads.clear()
            self.locks.clear()
            self.stop_events.clear()




class UtilApp(tk.Frame):
    def __init__(self, parent: tk.Widget, app_config: AppConfig, **kwargs):
        super().__init__(parent, **kwargs)

        self.app_config = app_config
        self.network_service = NetworkService(IPV4AddressConfiguration(), self.app_config)
        self.network_service.get_network_configuration()
        self.thread_service = ThreadManager()

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
