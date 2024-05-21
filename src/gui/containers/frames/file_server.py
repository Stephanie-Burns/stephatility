
import tkinter as tk
from tkinter import messagebox
from typing import Callable
from src.gui.containers.widgets import ToggleButton
from src.gui.containers.widgets.blue_label import BlueLabel

class FileServerRow(tk.Frame):
    def __init__(
            self,
            parent: tk.Widget,
            file_server: 'LocalFileServer',
            directory_var: tk.StringVar,
            **kwargs
    ) -> None:
        super().__init__(parent, **kwargs)
        self.file_server = file_server
        self.directory_var = directory_var

        self.config(bg="#7393B3")  #, borderwidth=2, relief="sunken")
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.port_label = BlueLabel(self, text="Port:")
        self.port_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 10))

        self.port_entry = tk.Entry(self, width=6, validate='key')
        self.port_entry['validatecommand'] = (self.port_entry.register(self.file_server.validate_port), '%P')
        self.port_entry.insert(0, '1337')
        self.port_entry.grid(row=0, column=1, sticky=tk.W, padx=(80, 0))

        self.server_label = BlueLabel(self, text="File Server [disable/enable]:")
        self.server_label.grid(row=0, column=2, sticky=tk.E, padx=(0, 75))

        self.server_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_file_server_toggle_change)
        self.server_toggle.grid(row=0, column=3, sticky=tk.E, pady=(10, 10), padx=(30, 10))

    def on_file_server_toggle_change(self) -> None:
        server_enabled = self.server_toggle.state

        if not self.file_server.validate_port(self.port_entry.get()):
            self.server_toggle.state = False
            messagebox.showerror("Invalid Port", "Please enter a valid port number (1-65535).")
            return

        if self.server_toggle and server_enabled:
            self.port_entry.configure(state="disabled")
            self._start_server()
        else:
            self.port_entry.configure(state="normal")
            self._stop_server()

    def _start_server(self) -> None:
        directory = self.directory_var.get()
        port = self.port_entry.get()

        try:
            self.file_server.start_server(directory, port)
        except ValueError as e:
            self.server_toggle.state = False
            messagebox.showerror("Error", str(e))

    def _stop_server(self) -> None:
        self.file_server.stop_server()
