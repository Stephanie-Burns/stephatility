
import os
import subprocess
import sys
import tempfile

import tkinter as tk
from tkinter import ttk
from typing import List

from src.application_config.logger import app_logger


class TempFileGenerator(tk.Frame):
    def __init__(self, parent: tk.Widget, file_extensions: List, **kwargs):
        super().__init__(parent, **kwargs)

        # Public Attributes
        self.file_extensions = file_extensions

        # Frame - TempFile Generator
        self.parent = parent
        self.grid(sticky=tk.EW, padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Dropdown - File Extension Select
        self.current_file_extension = tk.StringVar()
        self.file_extension_picker = ttk.Combobox(
            self,
            textvariable=self.current_file_extension,
            values=self.file_extensions,
            state='readonly',
            width=53
        )
        self.file_extension_picker.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.file_extension_picker.set(self.file_extensions[0])         # default value

        # Button - Create and Open
        self.create_open_button = tk.Button(
            self,
            text="Open Scratch File",
            command=self._create_and_open_scratch_file,
            width=20
        )
        self.create_open_button.grid(column=1, row=0, padx=10, pady=10, sticky=tk.E)

    def _create_and_open_scratch_file(self):
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=self.current_file_extension.get())
            temp_file.close()  # Close the file so it can be opened by another application

            if os.name == 'nt':
                os.startfile(temp_file.name)  # Works on Windows
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, temp_file.name])  # Works on macOS and Linux
        except Exception as e:
            app_logger.error(f"Failed to create or open scratch file: {e}")

def main():
    root = tk.Tk()
    root.title("Temp File Generator")
    app = TempFileGenerator(root)
    app.pack(fill='both', expand=True)

    # Set a minimum window size if desired
    root.minsize(400, 50)

    root.mainloop()


if __name__ == "__main__":
    main()
