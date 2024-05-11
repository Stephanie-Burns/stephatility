
import os
import subprocess
import sys
import tempfile

import tkinter as tk
from tkinter import ttk


class TempFileGenerator(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - TempFile Generator
        self.parent = parent
        self.grid(sticky='ew', padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Dropdown - File Extension Select
        self.all_file_extensions = ['.py', '.cs', '.md', '.txt']
        self.current_file_extension = tk.StringVar()
        self.file_extension_picker = ttk.Combobox(
            self,
            textvariable=self.current_file_extension,
            values=self.all_file_extensions,
            state='readonly',
            width=50
        )
        self.file_extension_picker.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.file_extension_picker.set(self.all_file_extensions[0])     # default value

        # Button - Create and Open
        self.create_open_button = tk.Button(
            self,
            text="Open Scratch File",
            command=self.create_and_open_scratch_file,
            width=20
        )
        self.create_open_button.grid(column=1, row=0, padx=10, pady=10, sticky=tk.E)

    def create_and_open_scratch_file(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=self.current_file_extension.get())
        temp_file.close()

        if os.name == 'nt':                         # For Windows
            os.startfile(temp_file.name)
        else:                                       # For Mac or Linux
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, temp_file.name])


def main():
    root = tk.Tk()
    root.title("Temp File Generator")
    app = TempFileGenerator(root)
    app.pack(fill='both', expand=True)

    # Set a minimum window size if desired
    root.minsize(400, 50)

    root.mainloop()


if __name__ == "__main__":
    main()
