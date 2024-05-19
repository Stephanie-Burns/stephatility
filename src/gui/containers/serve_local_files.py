
import os
import tkinter as tk

from typing import Optional
from urllib.parse import urlparse

import subprocess
import threading

from tkinter import filedialog, messagebox

from src.gui.containers.widgets import ToggleButton
from src.application_config.logger import app_logger


class ServeLocalFiles(tk.Frame):
    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.config(bg="#7393B3", borderwidth=2, relief="sunken")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        # Initialize instance attributes
        self.port_label         : Optional[tk.Label] = None
        self.port_entry         : Optional[tk.Entry] = None
        self.server_label       : Optional[tk.Label] = None
        self.server_toggle      : Optional[ToggleButton] = None

        self.hr_label           : Optional[tk.Label] = None
        self.hr_entry           : Optional[tk.Entry] = None
        self.hr_toggle          : Optional[ToggleButton] = None

        self.dir_label          : Optional[tk.Label] = None
        self.dir_entry          : Optional[tk.Entry] = None
        self.browse_button      : Optional[tk.Button] = None

        self.server_process = None
        self.server_thread = None

        # Create UI components
        self._create_row_file_server()
        self._create_row_hr_address()
        self._create_row_directory_picker()

    def _create_row_file_server(self) -> None:
        # Label - Port
        self.port_label = tk.Label(self, text="Port:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.port_label.grid(row=0, column=0, sticky="w", padx=(10, 10))

        # Entry - Port Number
        self.port_entry = tk.Entry(self, width=10, validate='key')
        self.port_entry['validatecommand'] = (self.port_entry.register(self._validate_port), '%P')
        self.port_entry.insert(0, '1337')
        self.port_entry.grid(row=0, column=1, sticky="w", padx=(10, 10))

        # Label - File Server
        self.server_label = tk.Label(
            self, text="File Server [disable/enable]:", fg='black', bg="#7393B3", font=("Arial", 14)
        )
        self.server_label.grid(row=0, column=2, sticky="e", padx=(0, 8))

        # Toggle - File Server State
        self.server_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_file_server_toggle_change)
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
        self.hr_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_hr_toggle_change)
        self.hr_toggle.grid(row=1, column=3, sticky="e", pady=(10, 10), padx=(0, 10))

    def _create_row_directory_picker(self) -> None:
        # Label - Directory to Serve
        self.dir_label = tk.Label(self, text="Directory to Serve:", fg='#010101', bg="#7393B3", font=("Arial", 14))
        self.dir_label.grid(row=2, column=0, sticky="w", padx=(10, 82), pady=(10, 10))

        # Entry - Directory Picker
        self.dir_entry = tk.Entry(self, width=48)
        self.dir_entry.insert(0, os.path.join(os.path.expanduser('~'), 'file-pile'))
        self.dir_entry.grid(row=2, column=1, columnspan=2, padx=(0, 0), pady=(10, 10))

        # Button - Browse
        self.browse_button = tk.Button(
            self, text="Browse", width=20, command=self._browse_directory, bg='#778da4', highlightbackground="black"
        )
        self.browse_button.grid(row=2, column=3, sticky="e", padx=(10, 10), pady=(10, 10))

    def _browse_directory(self) -> None:
        directory = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def on_file_server_toggle_change(self) -> None:

        server_enabled = self.server_toggle.state
        print(server_enabled)
        # if self.server_toggle and not self._validate_values():
        #     # self.server_toggle.toggle_off()
        #     return

        if not self._validate_values():
            self.server_toggle.state = False
            return

        if self.server_toggle and server_enabled:
            self.port_entry.configure(state="disabled")

            self.start_server()

        else:
            self.port_entry.configure(state="normal")

            self.stop_server()

    def on_hr_toggle_change(self) -> None:

        if self.hr_toggle and self.hr_toggle.state:
            self.hr_entry.configure(state='normal')
        else:
            self.hr_entry.configure(state='disabled')

    def start_server(self) -> None:
        directory = self.dir_entry.get()
        port = self.port_entry.get()

        if not directory:
            # self.server_toggle.toggle() TODO Find a better way
            messagebox.showerror("Error", "Please select a directory to serve.")
            app_logger.error("No directory selected.")
            return

        if not port.isdigit():
            # self.server_toggle.toggle()
            messagebox.showerror("Error", "Please enter a valid port number.")
            app_logger.error("Invalid port number entered.")
            return

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                app_logger.info(f"Directory created: {directory}")
            except OSError as e:
                # self.server_toggle.toggle()
                messagebox.showerror("Error", f"Failed to create directory: {e}")
                app_logger.error(f"Failed to create directory: {e}")
                return

        self.server_thread = threading.Thread(target=self.run_server, args=(directory, port))
        self.server_thread.start()
        app_logger.info(f"Server started in directory {directory} on port {port}")

    def run_server(self, directory: str, port: int) -> None:
        os.chdir(directory)
        self.server_process = subprocess.Popen(["python", "-m", "http.server", port])
        app_logger.info(f"Serving HTTP on {directory} port {port}")

    def stop_server(self) -> None:
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            app_logger.info("Server process terminated.")

    def _validate_port(self, port: str) -> bool:
        """Validate port entry to ensure it is an integer within the valid range."""
        if port.isdigit():
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return True
        return False

    def _validate_url(self, url: str) -> bool:
        """Validate the URL to ensure it is a valid web address."""
        result = urlparse(url)
        if result.scheme and result.netloc:
            return True
        if not result.scheme and result.path:
            # Handle local domain names like sharebear.local
            if '.' in result.path and result.path.split('.')[0] and result.path.split('.')[-1]:
                return True
        return False

    def _validate_values(self) -> bool:
        current_directory = self.dir_entry.get()
        port_value = self.port_entry.get()
        url_value = self.hr_entry.get()

        if not self._validate_port(port_value):
            # self.server_toggle.toggle()
            messagebox.showerror("Invalid Port", "Please enter a valid port number (1-65535).")
            return False

        if not self._validate_url(url_value):
            # self.server_toggle.toggle()
            messagebox.showerror("Invalid URL", "Please enter a valid web address.")
            return False

        print(f'Selected Directory: {current_directory}')
        print(f'Port: {port_value}')
        print(f'URL: {url_value}')

        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HTTP Server Utility")

    app = ServeLocalFiles(root)
    app.pack()

    root.mainloop()
