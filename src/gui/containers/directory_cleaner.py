
import os
import shutil

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List

from src.application_config.logger import app_logger


class DirectoryCleaner(tk.Frame):
    def __init__(self, parent, uid: int, directories_to_delete: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        self.uid = uid
        self.directories_to_delete = directories_to_delete

        # Frame - Directory Cleaner
        self.grid(sticky='ew', padx=10, pady=10)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Entry - Path Entry
        self.path_entry = tk.Entry(self, width=50)
        self.path_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)
        self.path_entry.insert(0, self.directories_to_delete[self.uid])

        # Button - Browse
        self.browse_button = tk.Button(
            self,
            text="Browse",
            command=self._browse_folder,
            width=20
        )
        self.browse_button.grid(row=0, column=2, padx=10, sticky=tk.EW)

        # Button - Delete Contents
        self.delete_button = tk.Button(
            self,
            text="Delete Contents",
            command=self._delete_contents,
            width=20
        )
        self.delete_button.grid(row=0, column=3, padx=10, sticky=tk.EW)

    def _browse_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.path_entry.get())
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)
            self.directories_to_delete[self.uid] = folder_selected

    def _delete_contents(self) -> None:
        folder = self.path_entry.get()

        if not os.path.isdir(folder):
            app_logger.debug("The specified directory doesn't exist: %s", folder)
            messagebox.showerror("Error", "The specified directory does not exist.")
            return

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete all contents in {folder}?"):
            return

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
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

        app_logger.info("Contents deleted successfully: %s", folder)
        messagebox.showinfo("Success", "Contents deleted successfully.")


def main():
    root = tk.Tk()
    root.title("Directory Cleaner")

    default_path = "/path/to/initial/directory"
    app = DirectoryCleaner(root, 0, default_path)
    app.pack(fill='both', expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
