
import os
import shutil

import tkinter as tk
from tkinter import messagebox, ttk

from src.application_config.app_logger import app_logger
from src.constants import Colors
from src.gui.containers.widgets.directory_picker import DirectoryPicker
from src.gui.containers.widgets.tooltip import add_tooltip
from src.engine.file_center.file_center_settings import FileCenterSettings


class DirectoryCleaner(tk.Frame):
    def __init__(
            self,
            parent,
            uid: int = 0,
            user_settings: FileCenterSettings = None,
            **kwargs
    ):
        super().__init__(parent, background=Colors.BLUE_GRAY, **kwargs)
        self._user_settings = user_settings

        self.uid = uid

        # Frame - Self
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Frame - Directory Picker
        self.directory_picker = DirectoryPicker(self, update_callback=self._on_directory_picker_change)
        self.directory_picker.set_directory(self.load_user_directory())
        self.directory_picker.grid(row=0, column=0, sticky=tk.EW)

        # Button - Delete Contents
        self.delete_button = ttk.Button(
            self,
            text="Delete Contents",
            style="Blue.TButton",
            width=20,
            command=self._delete_contents,
        )
        self.delete_button.grid(row=0, column=2, padx=(10, 0), sticky=tk.EW)
        tooltip_message = ('Delete all files and directories in the selected path.\n'
                           'This action is irreversible.')
        add_tooltip(self.delete_button, text=tooltip_message, position=tk.S, offset_x=0)

    def _on_directory_picker_change(self) -> None:
        self.save_user_directory(self.directory_picker.get_directory())

    def _delete_contents(self) -> None:
        directory = self.directory_picker.get_directory()

        if not directory or not os.path.isdir(directory):
            app_logger.debug("The specified directory doesn't exist: '%s'", directory)
            messagebox.showerror("Error", "The specified directory does not exist.")
            return

        prompt = f"Are you sure you want to delete all contents in {directory}?"
        if not messagebox.askyesno("Confirm", prompt):
            return

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                app_logger.debug("Deleted %s", item_path)

            except Exception as e:
                app_logger.debug("Failed to delete: %s", item_path, exc_info=True)
                messagebox.showerror("Error", f"Failed to delete {item_path}: {e}")
                continue

        self.save_user_directory(directory)

        app_logger.info("Contents deleted successfully: %s", directory)
        messagebox.showinfo("Success", "Contents deleted successfully.")

    def save_user_directory(self, directory) -> None:
        if self._user_settings is not None:
            self._user_settings.set_directory_to_police(self.uid, directory)

    def load_user_directory(self) -> str:
        return self._user_settings.get_directory_to_police(self.uid) if self._user_settings is not None else ''


class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Directory Cleaner Demo")
        self.geometry("400x100")

        configure_styles()
        initialize_icons()

        self.directory_cleaner = DirectoryCleaner(self, 0)
        self.directory_cleaner.pack(fill=tk.X, padx=10, pady=10)


if __name__ == '__main__':
    from src.gui.styles import configure_styles
    from src.application_config.icon_setup import initialize_icons

    app = DemoApp()
    app.mainloop()
