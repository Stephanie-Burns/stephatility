
import tkinter as tk
from src.gui import DirectoryCleaner, TempFileGenerator
from src.engine.file_center.file_center_settings import FileCenterSettings


class FileCenter(tk.Frame):
    def __init__(self, parent: tk.Widget, user_settings: FileCenterSettings, **kwargs) -> None:
        super().__init__(parent, borderwidth=2, relief="sunken", **kwargs)

        self.user_settings = user_settings

        # Frame - Self
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Frame - Directory Cleaner
        self.directory_cleaner_0 = DirectoryCleaner(self, uid=0, user_settings=self.user_settings)
        self.directory_cleaner_0.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=5)

        # Frame - Tempfile Generator
        self.tempfile_gen01 = TempFileGenerator(self, uid=0, user_settings=self.user_settings)
        self.tempfile_gen01.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=5)

        # Frame - Directory Cleaner
        self.directory_cleaner_1 = DirectoryCleaner(self, uid=1, user_settings=self.user_settings)
        self.directory_cleaner_1.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=5)

        # Frame - Tempfile Generator
        self.tempfile_gen02 = TempFileGenerator(self, uid=1, user_settings=self.user_settings)
        self.tempfile_gen02.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=5)

    def on_close(self):
        """Handle any cleanup necessary when the FileCenter is closed."""
        pass
