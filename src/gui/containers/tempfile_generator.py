
import os
import subprocess
import sys
import tempfile

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from src.constants import ASSETS_DIR
from src.application_config.logger import app_logger

from src.gui.containers.frames.item_manager import ItemManager


class TempFileGenerator(tk.Frame):
    def __init__(self, parent: tk.Widget, file_extensions: List, **kwargs):
        super().__init__(parent, **kwargs)

        # Public Attributes
        self.file_extensions = file_extensions

        # Frame - TempFile Generator
        self.parent = parent
        self.grid(sticky=tk.EW, padx=10, pady=10)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        # Dropdown - File Extension Select
        self.current_file_extension = tk.StringVar()
        self.file_extension_picker = ttk.Combobox(
            self,
            textvariable=self.current_file_extension,
            values=self.file_extensions,
            state='readonly',
            width=52
        )
        self.file_extension_picker.grid(column=0, columnspan=2, row=0, padx=10, pady=10, sticky=tk.W)
        self.file_extension_picker.set(self.file_extensions[0])

        # Button - Manage
        self.manage = tk.Button(
            self,
            text="Manage",
            command=self._on_manage_action,
            width=21
        )
        self.manage.grid(column=2, row=0, padx=10, pady=10, sticky=tk.E)

        # Button - Create and Open
        self.create_open_button = tk.Button(
            self,
            text="Open Scratch File",
            command=self._create_and_open_scratch_file,
            width=20
        )
        self.create_open_button.grid(column=3, row=0, padx=10, pady=10, sticky=tk.E)

    def _on_manage_action(self):
        icon_path = str(ASSETS_DIR / "file.png")
        item_manager = ItemManager(self, item_type="Extension", icon=icon_path, file_extensions=self.file_extensions)
        item_manager.set_items(self.file_extensions)

        self.wait_window(item_manager)
        self.file_extension_picker.config(values=self.file_extensions)
        self.file_extension_picker.set(self.file_extensions[0])



    def _create_and_open_scratch_file(self):
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=self.current_file_extension.get())
            temp_file.close()

            if os.name == 'nt':
                os.startfile(temp_file.name)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, temp_file.name])
        except Exception as e:
            app_logger.error(f"Failed to create or open scratch file: {e}")
            messagebox.showerror("Error", f"Failed to create or open scratch file: {e}")

def main():
    root = tk.Tk()
    root.title("Temp File Generator")
    app = TempFileGenerator(root)
    app.pack(fill='both', expand=True)

    root.minsize(400, 50)

    root.mainloop()


if __name__ == "__main__":
    main()
