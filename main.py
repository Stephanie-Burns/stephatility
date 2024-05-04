
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import tempfile
import subprocess
import sys

from widget_ip_manager import IPManagerWidget
from octet_widget import OctletWidget

class FolderCleanerApp:
    def __init__(self, master):
        self.current_ip = '192.168.1.100'  # This would ideally come from a configuration or external source

        # Initialize other rows of widgets
        self.initialize_dir_destruction_row(master, "C:/Viper", 0)
        self.initialize_dir_destruction_row(master, "C:/ViperConfigData", 1)
        self.initialize_file_creation_row(master, ['.py', '.cs', '.md', '.txt'], 2)

        # Initialize IP Manager Widget
        self.ip_manager = IPManagerWidget(master, 3, self.current_ip)


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

    def ensure_valid_entry(self, event, entry, index):
        """ Ensure that each entry field has a valid IP address segment or set it to the respective current IP part. """
        if not entry.get() or not self.validate_ip_part(entry.get()):
            entry.delete(0, tk.END)
            # Insert the current IP octet if valid, else default to '1'
            entry.insert(0, self.current_ip[index] if self.current_ip[index].isdigit() and self.validate_ip_part(
                self.current_ip[index]) else '1')

    def clear_entry(self, entry):
        """ Clear the entry field when clicked. """
        entry.delete(0, tk.END)

    def get_current_ip(self):
        # Mock-up function; replace this with your actual method to get the current IP
        return '192.168.1.100'

    def validate_ip_part(self, P):
        """ Validate the entry for IP parts. Allow only digits, limit to 255, and exclude 0 and 255. """
        if P == "":
            return True  # Allow clearing the entry
        if P.isdigit():
            num = int(P)
            if 0 < num < 255:  # Excluding 0 and 255 from being valid inputs
                return True
        return False

    def handle_key_press(self, event, ip_parts, index):
        """Handle the key press event to automatically advance under specific conditions."""
        current_entry_content = ip_parts[index].get()

        # Automatically advance if the user inputs three digits and it's valid
        if len(current_entry_content) == 2 and event.char.isdigit():
            potential_new_content = current_entry_content + event.char
            if self.validate_ip_part(potential_new_content):
                ip_parts[index].delete(0, tk.END)  # Clear the current input
                ip_parts[index].insert(0, potential_new_content)  # Insert the new valid input
                # Advance focus based on the index
                if index < len(ip_parts) - 1:
                    ip_parts[index + 1].focus()
                else:
                    self.set_button.focus()  # Directly set focus to the set_button
                return "break"  # Prevent further input in the current entry box

        # Handle period to advance without inserting it, only if the current entry is valid and not empty
        elif event.char == '.':
            if current_entry_content and self.validate_ip_part(current_entry_content):
                if index < len(ip_parts) - 1:
                    ip_parts[index + 1].focus()
                else:
                    self.set_button.focus()  # Directly set focus to the set_button
                return "break"  # Prevent the period from being inserted

    def set_ip_address(self, ip_parts):
        # Validate and possibly refill each part before setting the IP address
        self.validate_and_refill_parts(ip_parts)
        ip_address = '.'.join(part.get() for part in ip_parts)
        print("Setting IP Address:", ip_address)  # Placeholder for actual set IP function

    def validate_and_refill_parts(self, ip_parts):
        """ Ensure all parts are valid before setting the IP, refill if necessary. """
        for i, part in enumerate(ip_parts):
            if not part.get() or not self.validate_ip_part(part.get()):
                # Refill the entry with the current IP octet or default to '1'
                part.delete(0, tk.END)
                part.insert(0, self.current_ip[i] if self.current_ip[i].isdigit() and self.validate_ip_part(
                    self.current_ip[i]) else '1')

    def manage_ip_settings(self):
        # Open a new window to manage IP settings
        manage_window = tk.Toplevel(self.master)
        manage_window.title("IP Settings")
        tk.Label(manage_window, text="IP Settings Management").pack()


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
