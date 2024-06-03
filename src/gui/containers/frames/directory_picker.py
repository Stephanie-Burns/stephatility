import tkinter as tk
import os
from tkinter import filedialog
import subprocess

from src.gui.containers.widgets.blue_label import BlueLabel
from src.gui.containers.widgets.blue_button import BlueButton



# !!!!! Dep this when networck center directory pickeer is updated.
class DirectoryPickerRow(tk.Frame):
    def __init__(self, parent: tk.Widget, directory_var: tk.StringVar, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.directory_var = directory_var

        self.config(bg="#7393B3")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        self.dir_label = BlueLabel(self, text="Directory to Serve:")
        self.dir_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 82), pady=(10, 10))

        self.dir_entry = tk.Entry(self, width=48, textvariable=self.directory_var)
        self.dir_entry.grid(row=0, column=1, columnspan=2, padx=(0, 5), pady=(10, 10))

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self, bg="#7393B3")
        self.button_frame.grid(row=0, column=3, sticky=tk.E, padx=(10, 10), pady=(10, 10))

        self.browse_button = BlueButton(self.button_frame, text="Browse", width=7, command=self._browse_directory)
        self.browse_button.grid(row=0, column=0, sticky=tk.W, padx=(6, 11))

        self.open_button = BlueButton(self.button_frame, text="Open", width=7, command=self._open_directory)
        self.open_button.grid(row=0, column=1, sticky=tk.E)

    def _browse_directory(self) -> None:
        directory = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def _open_directory(self) -> None:
        directory = self.dir_entry.get()
        if os.path.isdir(directory):
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(directory)
                elif os.uname().sysname == 'Darwin':  # For macOS
                    subprocess.call(['open', directory])
                else:  # For Linux and other UNIX-like OSes
                    subprocess.call(['xdg-open', directory])
            except Exception as e:
                print(f"Failed to open directory: {e}")
