
import os
import subprocess
import sys
import tempfile
from typing import List
import tkinter as tk
from tkinter import ttk, messagebox

from src.application_config.app_logger import app_logger
from src.constants import Colors
from src.application_config.icon_setup import IconManager
from src.engine.file_center.file_center_settings import FileCenterSettings
from src.gui.containers.widgets.single_column_item_manager import SingleColumnItemManager
from src.gui.containers.widgets.tooltip import add_tooltip


class TempFileGenerator(tk.Frame):
    def __init__(
            self,
            parent          : tk.Misc,
            uid             : int = 0,
            user_settings   : FileCenterSettings = None,
            **kwargs,
         ):
        super().__init__(parent, background=Colors.BLUE_GRAY, **kwargs)
        self.uid = uid
        self.icon_manager = IconManager()
        self._user_settings = user_settings

        self.selected_file_extension = tk.StringVar()
        self._extension_manager = None

        # Frame - Self
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Dropdown - File Extension Select
        self.file_extension_picker = ttk.Combobox(
            self,
            style='Blue.TCombobox',
            textvariable=self.selected_file_extension,
            values=[],
            state='readonly',
        )
        self.file_extension_picker.grid(column=0, row=0, padx=(0, 0), pady=(0, 0), sticky=tk.EW)
        self._update_combobox()

        # Button - Manage
        self.manage_button = ttk.Button(
            self,
            text="Manage",
            style="Blue.TButton",
            command=self._on_manage_clicked,
        )
        self.manage_button.grid(column=1, row=0, padx=(0, 10), pady=(0, 0), sticky=tk.EW)
        self.manage_button.config(image=self.icon_manager.get_icon('config', (16, 16)))
        add_tooltip(self.manage_button, text='Manage file extension list', position=tk.S)

        # Button - Create and Open
        self.create_open_button = ttk.Button(
            self,
            text="Open Scratch File",
            style="Blue.TButton",
            command=self._create_and_open_scratch_file,
        )
        self.create_open_button.grid(column=2, row=0, padx=(10, 0), pady=(0, 0), sticky=tk.EW)
        tooltip_message = ('Create and open a temporary file with the selected extension.\n'
                           'The file will be deleted by the system when no longer needed.')
        add_tooltip(self.create_open_button, text=tooltip_message, position=tk.S, offset_x=-290)

    def _on_manage_clicked(self):
        if self._extension_manager is None or not tk.Toplevel.winfo_exists(self._extension_manager):
            self._extension_manager = SingleColumnItemManager(
                self,
                item_type="Extension",
                icon=self.icon_manager.get_icon('browse_folder', (16, 16)),
                items=self.load_user_extensions(),
                update_callback=self._on_manage_closed
            )
            self._extension_manager.set_items(self.load_user_extensions())

            self.wait_window(self._extension_manager)

        else:
            self._extension_manager.lift()
            self._extension_manager.focus_set()

    def _on_manage_closed(self):
        self.save_user_extensions(self._extension_manager.get_items())
        self._update_combobox()

        if self._extension_manager:
            self._extension_manager = None

    def _create_and_open_scratch_file(self):
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=self.selected_file_extension.get())
            temp_file.close()

            if os.name == 'nt':
                os.startfile(temp_file.name)

            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, temp_file.name])

        except Exception as e:
            app_logger.error(f"Failed to create or open scratch file: {e}")
            messagebox.showerror("Error", f"Failed to create or open scratch file: {e}")

    def _update_combobox(self) -> None:

        saved_extensions_list = self.load_user_extensions()

        if saved_extensions_list:
            selected_extension = self.load_user_extensions()[0]
            self.file_extension_picker.set(selected_extension)
        else:
            self.file_extension_picker.set('')

        self.file_extension_picker.config(values=saved_extensions_list)

    def save_user_extensions(self, extensions: List[str]) -> None:
        if self._user_settings is None:
            return

        self._user_settings.set_temp_file_extensions(self.uid, extensions)

    def load_user_extensions(self) -> List[str]:
        if self._user_settings is None:
            return ['.txt']

        return self._user_settings.get_temp_file_extensions(self.uid)


class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TempFile Generator Demo")
        self.geometry("400x100")
        self.configure(background=Colors.BLUE_GRAY)

        configure_styles()
        initialize_icons()

        self.temp_file_gen = TempFileGenerator(self, uid=0, user_settings=FileCenterSettings())
        self.temp_file_gen.pack(fill=tk.X, padx=10, pady=10)


if __name__ == '__main__':
    from src.application_config.icon_setup import initialize_icons
    from src.gui.styles import configure_styles

    app = DemoApp()
    app.mainloop()
