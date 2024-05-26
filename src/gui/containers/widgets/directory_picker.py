
import os
import tkinter as tk

from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional

from src.application_config.app_logger import app_logger
from src.constants import Colors
from src.gui.containers.widgets.tooltip import ToolTip
from src.gui.icon_manager import IconManager
from src.gui.mixins import CallbackMixin


class DirectoryPicker(CallbackMixin, tk.Frame):
    def __init__(self, parent: tk.Widget, update_callback: Optional[Callable[..., None]], *args, **kwargs):
        super().__init__(update_callback, parent, *args, **kwargs)

        # Frame - DirectoryPicker
        self.configure(background=Colors.BLUE_GRAY)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.icon_manager = IconManager()

        self.directory = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self) -> None:
        # Entry - Selected directory
        self.selected_directory = tk.Entry(self, textvariable=self.directory, relief=tk.SUNKEN)
        self.selected_directory.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))

        # Button - Open the directory picker dialog
        self.pick_button = ttk.Button(self, style="Blue.TButton", command=self._pick_directory)
        self.pick_button.grid(row=0, column=1, padx=(0, 0), sticky=tk.EW)
        self.pick_button.config(image=self.icon_manager.get_icon('browse_folder', (16, 16)))
        ToolTip(self.pick_button, 'Pick a directory', tk.S, offset_x=-40)

        # Button - Open the selected directory in file explorer
        self.explorer_button = ttk.Button(self, style="Blue.TButton", command=self._open_in_explorer)
        self.explorer_button.grid(row=0, column=2, sticky=tk.EW,)
        self.explorer_button.config(image=self.icon_manager.get_icon('live_folder', (16, 16)))
        ToolTip(self.explorer_button, 'Open directory', tk.S, offset_x=-70)

    def _pick_directory(self) -> None:
        directory = filedialog.askdirectory()
        if directory:
            self.set_directory(directory)

    def _open_in_explorer(self) -> None:
        directory = self.get_directory()
        if directory and os.path.isdir(directory):
            if os.name == 'nt':  # Windows
                os.startfile(directory)
            elif os.name == 'posix':  # Linux
                try:
                    os.system(f'xdg-open "{directory}"')
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open directory: {e}")
            else:
                messagebox.showerror("Unsupported OS", "This feature is not supported on your operating system.")
        else:
            messagebox.showwarning("Invalid Directory", "Please select a valid directory first.")

    def get_directory(self) -> str:
        """Returns the currently selected directory."""
        return self.directory.get()

    def set_directory(self, directory: str) -> None:
        """Sets the directory to the given value."""
        if os.path.isdir(directory):
            self.directory.set(directory)
            self.emit_update()
        else:
            app_logger.debug("Attempted to set invalid directory: '%s'", directory)


class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Directory Picker Demo")
        self.geometry("400x100")
        self.configure(background=Colors.BLUE_GRAY)

        configure_styles()
        initialize_icons()

        self.directory_picker = DirectoryPicker(self)
        self.directory_picker.pack(fill=tk.X, padx=10, pady=10)
        self.directory_picker.set_directory('/usr')


if __name__ == '__main__':
    from src.gui.styles import configure_styles
    from src.application_config.icon_setup import initialize_icons

    app = DemoApp()
    app.mainloop()
