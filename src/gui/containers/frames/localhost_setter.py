import tkinter as tk
from tkinter import messagebox
from src.gui.containers.widgets import ToggleButton

class HRAddressRow(tk.Frame):
    def __init__(self, parent: tk.Widget, file_server: 'LocalFileServer', app_config, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.file_server = file_server
        self.app_config = app_config

        self.config(bg="#7393B3") #, borderwidth=2, relief="sunken")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        self.hr_label = tk.Label(self, text="Human Readable Address:", fg='black', bg="#7393B3", font=("Arial", 14))
        self.hr_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 0))

        self.hr_entry = tk.Entry(self, width=48)
        self.hr_entry.insert(0, self._get_friendly_name())
        self.hr_entry.grid(row=0, column=1, columnspan=2, padx=(10, 10))

        self.hr_toggle = ToggleButton(self, initial_state=False, update_callback=self.on_hr_toggle_change)
        self.hr_toggle.grid(row=0, column=3, sticky=tk.E, pady=(10, 10), padx=(0, 10))

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
