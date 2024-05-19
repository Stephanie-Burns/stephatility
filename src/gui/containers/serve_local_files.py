
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional

from src.gui.containers.widgets import ToggleButton


class ServeLocalFiles(tk.Frame):
    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.config(bg="#7393B3", borderwidth=2, relief="sunken")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        # Initialize instance attributes
        self.port_label       : Optional[tk.Label] = None
        self.port_entry       : Optional[tk.Entry] = None
        self.server_label     : Optional[tk.Label] = None
        self.server_toggle    : Optional[ToggleButton] = None

        self.hr_label          : Optional[tk.Label] = None
        self.hr_entry          : Optional[tk.Entry] = None
        self.hr_toggle         : Optional[ToggleButton] = None

        self.dir_label         : Optional[tk.Label] = None
        self.dir_entry         : Optional[tk.Entry] = None
        self.browse_button     : Optional[tk.Button] = None

        # Create UI components
        self._create_row_file_server()
        self._create_row_hr_address()
        self._create_row_directory_picker()

    def _create_row_file_server(self) -> None:
        # Label - Port
        self.port_label = tk.Label(self, text="Port:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.port_label.grid(row=0, column=0, sticky="w", padx=(10, 10))

        # Entry - Port Number
        self.port_entry = tk.Entry(self, width=10)
        self.port_entry.grid(row=0, column=1, sticky="w", padx=(10, 10))
        self.port_entry.insert(0, '1337')

        # Label - File Server
        self.server_label = tk.Label(
            self, text="File Server [disable/enable]:", fg='black', bg="#7393B3", font=("Arial", 14)
        )
        self.server_label.grid(row=0, column=2, sticky="e", padx=(0, 8))

        # Toggle - File Server State
        self.server_toggle = ToggleButton(self, initial_state=False)
        self.server_toggle.grid(row=0, column=3, sticky="e", pady=(10, 10), padx=(0, 10))

    def _create_row_hr_address(self) -> None:
        # Label - Human Readable Address
        self.hr_label = tk.Label(self, text="Human Readable Address:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.hr_label.grid(row=1, column=0, sticky="w", padx=(10, 0))

        # Entry - HR Local Server Address
        self.hr_entry = tk.Entry(self, width=48)
        self.hr_entry.insert(0, "sharebear.local")
        self.hr_entry.config(state="disabled")
        self.hr_entry.grid(row=1, column=1, columnspan=2, padx=(10, 10))

        # Toggle - Human Readable Address
        self.hr_toggle = ToggleButton(self, initial_state=False)
        self.hr_toggle.grid(row=1, column=3, sticky="e", pady=(10, 10), padx=(0, 10))

    def _create_row_directory_picker(self) -> None:
        # Label - Directory to Serve
        self.dir_label = tk.Label(self, text="Directory to Serve:", fg='#010101', bg="#7393B3", font=("Arial", 14))
        self.dir_label.grid(row=2, column=0, sticky="w", padx=(10, 82), pady=(10, 10))

        # Entry - Directory Picker
        self.dir_entry = tk.Entry(self, width=48)
        self.dir_entry.insert(0, os.path.join(os.path.abspath(os.sep), 'file-pile'))
        self.dir_entry.grid(row=2, column=1, columnspan=2, padx=(0, 0), pady=(10, 10))

        # Button - Browse
        self.browse_button = tk.Button(
            self, text="Browse", width=20, command=self._browse_directory, bg='#778da4', highlightbackground="black"
        )
        self.browse_button.grid(row=2, column=3, sticky="e", padx=(10, 10), pady=(10, 10))

    def _browse_directory(self) -> None:
        directory = filedialog.askdirectory(initialdir=os.path.abspath(os.sep))
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HTTP Server Utility")

    app = ServeLocalFiles(root)
    app.pack()

    root.mainloop()
