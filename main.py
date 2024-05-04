
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import tempfile
import subprocess
import sys

from octet_widget import OctetWidget, IPManagerWidget


class FolderCleanerApp:
    def __init__(self, master):
        master.title('ViperTility') # fix this
        self.current_ip = '192.168.1.100'  # This would ideally come from a configuration or external source

        # Initialize other rows of widgets
        self.initialize_dir_destruction_row(master, "C:/Viper", 0)
        self.initialize_dir_destruction_row(master, "C:/ViperConfigData", 1)
        self.initialize_file_creation_row(master, ['.py', '.cs', '.md', '.txt'], 2)

        # Initialize IP Manager Widget
        self.ip_manager = IPManagerWidget(master, self.current_ip, 3)

    def initialize_file_creation_row(self, master, extensions, row):
        # Dropdown for file extensions
        file_extension = tk.StringVar()

        extension_picker = ttk.Combobox(
            master,
            textvariable=file_extension,
            values=extensions,
            state='readonly'
        )
        # Button to create and open scratch file
        create_open_button = tk.Button(
            master,
            text="Create and Open Scratch File",
            command=lambda: self.create_and_open_scratch_file(file_extension)
        )

        extension_picker.grid(row=row, column=1, padx=10, pady=10, sticky=tk.EW)
        create_open_button.grid(row=row, column=2, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        extension_picker.set(extensions[0])  # default value

    @staticmethod
    def initialize_dir_destruction_row(master, default_path, row):
        path_entry = tk.Entry(master, width=50)

        browse_button = tk.Button(
            master,
            text="Browse",
            command=lambda: FolderCleanerApp.browse_folder(path_entry)
        )
        delete_button = tk.Button(
            master,
            text="Delete Contents",
            command=lambda: FolderCleanerApp.delete_contents(path_entry)
        )

        path_entry.grid(row=row, column=1, padx=10, pady=10, sticky=tk.EW)
        browse_button.grid(row=row, column=2, padx=10, sticky=tk.EW)
        delete_button.grid(row=row, column=3, padx=10, sticky=tk.EW)

        path_entry.insert(0, default_path)

    @staticmethod
    def browse_folder(path_entry):
        folder_selected = filedialog.askdirectory(initialdir=path_entry.get())
        if folder_selected:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, folder_selected)

    @staticmethod
    def delete_contents(path_entry):
        folder = path_entry.get()
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete all contents in {folder}?"):
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            messagebox.showinfo("Success", "Contents deleted successfully.")

    @staticmethod
    def create_and_open_scratch_file(file_extension):
        ext = file_extension.get()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        temp_file.close()
        if os.name == 'nt':                         # For Windows
            os.startfile(temp_file.name)
        else:                                       # For Mac or Linux
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, temp_file.name])


def main():
    root = tk.Tk()
    app = FolderCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
