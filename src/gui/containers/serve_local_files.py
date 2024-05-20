
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

from src.gui.containers.widgets import ToggleButton
from src.application_config.logger import app_logger


class ServeLocalFiles(tk.Frame):
    def __init__(self, parent: tk.Widget, file_server: 'LocalFileServer', app_config, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.app_config = app_config

        self.config(bg="#7393B3", borderwidth=2, relief="sunken")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        # Initialize instance attributes
        self.port_label: Optional[tk.Label] = None
        self.port_entry: Optional[tk.Entry] = None
        self.server_label: Optional[tk.Label] = None
        self.server_toggle: Optional[ToggleButton] = None

        self.hr_label: Optional[tk.Label] = None
        self.hr_entry: Optional[tk.Entry] = None
        self.hr_toggle: Optional[ToggleButton] = None

        self.dir_label: Optional[tk.Label] = None
        self.dir_entry: Optional[tk.Entry] = None
        self.browse_button: Optional[tk.Button] = None

        self.file_server = file_server

        # Create UI components
        self._create_row_file_server()
        self._create_row_hr_address()
        self._create_row_directory_picker()

    # GUI Setup

    def _create_row_file_server(self) -> None:
        # Label - Port
        self.port_label = tk.Label(self, text="Port:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.port_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 10))

        # Entry - Port Number
        self.port_entry = tk.Entry(self, width=10, validate='key')
        self.port_entry['validatecommand'] = (self.port_entry.register(self.file_server.validate_port), '%P')
        self.port_entry.insert(0, '1337')
        self.port_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 10))

        # Label - File Server
        self.server_label = tk.Label(
            self, text="File Server [disable/enable]:", fg='black', bg="#7393B3", font=("Arial", 14)
        )
        self.server_label.grid(row=0, column=2, sticky=tk.E, padx=(0, 8))

        # Toggle - File Server State
        self.server_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_file_server_toggle_change)
        self.server_toggle.grid(row=0, column=3, sticky=tk.E, pady=(10, 10), padx=(0, 10))

    def _create_row_hr_address(self) -> None:
        # Label - Human Readable Address
        self.hr_label = tk.Label(self, text="Human Readable Address:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.hr_label.grid(row=1, column=0, sticky=tk.W, padx=(10, 0))

        # Entry - HR Local Server Address
        self.hr_entry = tk.Entry(self, width=48)
        self.hr_entry.insert(0, self._get_friendly_name())
        self.hr_entry.grid(row=1, column=1, columnspan=2, padx=(10, 10))

        # Toggle - Human Readable Address
        self.hr_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_hr_toggle_change)
        self.hr_toggle.grid(row=1, column=3, sticky=tk.E, pady=(10, 10), padx=(0, 10))

    def _create_row_directory_picker(self) -> None:
        # Label - Directory to Serve
        self.dir_label = tk.Label(self, text="Directory to Serve:", fg='#010101', bg="#7393B3", font=("Arial", 14))
        self.dir_label.grid(row=2, column=0, sticky=tk.W, padx=(10, 82), pady=(10, 10))

        # Entry - Directory Picker
        self.dir_entry = tk.Entry(self, width=48)
        self.dir_entry.insert(0, os.path.join(os.path.expanduser('~'), 'file-pile'))
        self.dir_entry.grid(row=2, column=1, columnspan=2, padx=(0, 0), pady=(10, 10))

        # Button - Browse
        self.browse_button = tk.Button(
            self, text="Browse", width=20, command=self._browse_directory, bg='#778da4', highlightbackground="black"
        )
        self.browse_button.grid(row=2, column=3, sticky=tk.E, padx=(10, 10), pady=(10, 10))

    def _browse_directory(self) -> None:
        directory = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    # Events

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

    def on_hr_toggle_change(self) -> None:
        local_address = self.hr_entry.get()

        if not self.file_server.validate_url(local_address):
            self.hr_toggle.state = False
            self.hr_entry.configure(state="normal")
            messagebox.showerror(
                "Invalid Domain",
                "Please enter a valid local domain.\n"
                "(e.g., sharebear.local)\n\n"
                "Allowed characters:\n"
                "- Alphanumerics\n"
                "- Dots\n"
                "- Dashes\n"
                "- Underscores"
            )
            return

        if self.hr_toggle.state:
            self.hr_entry.configure(state='disabled')
            self._set_friendly_name(local_address)
        else:
            self.hr_entry.configure(state='normal')

    # Actions

    def _start_server(self) -> None:
        directory = self.dir_entry.get()
        port = self.port_entry.get()

        try:
            self.file_server.start_server(directory, port)
        except ValueError as e:
            self.server_toggle.state = False
            messagebox.showerror("Error", str(e))

    def _stop_server(self) -> None:
        self.file_server.stop_server()

    def _get_friendly_name(self) -> str:
        import random

        if not self.app_config.user_server_name:
            return random.choice(self.app_config.default_server_names)
        else:
            return self.app_config.user_server_name

    def _set_friendly_name(self, new_friendly_name: str) -> None:
        try:
            self.file_server.set_friendly_name(new_friendly_name, self.app_config.user_server_name)
            self.app_config.user_server_name = new_friendly_name

        except PermissionError as e:
            self._handle_hr_exception("Permission Error", str(e))

        except OSError as e:
            self._handle_hr_exception("File Error", str(e))

        except Exception as e:
            self._handle_hr_exception("Error", str(e))

    def _handle_hr_exception(self, title: str, message: str) -> None:
        self.hr_toggle.state = False
        self.hr_entry.configure(state="normal")
        messagebox.showerror(title, message)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HTTP Server Utility")
    #
    # thread_manager = ThreadManager()
    # server_backend = ServerBackend(thread_manager)
    # app = ServeLocalFiles(root, server_backend)
    # app.pack()

    root.mainloop()
