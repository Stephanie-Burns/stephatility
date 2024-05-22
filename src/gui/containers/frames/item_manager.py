
import tkinter as tk
from tkinter import ttk, messagebox

from src.constants import Colors, ASSETS_DIR
from src.gui.containers.widgets.draggable_treeview import DraggableTreeview
from src.gui.containers.widgets.blue_button import BlueButton


class ItemManager(tk.Toplevel):
    def __init__(self, parent=None, item_type="Item", icon=None, **kwargs):
        super().__init__(parent, borderwidth=2, relief="raised", bg=Colors.ORBITAL, **kwargs)
        self.item_type = item_type
        self.title(f"{item_type} Manager")
        self.geometry("500x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        if icon:
            self.icon = tk.PhotoImage(file=str(icon))
            self.iconphoto(False, self.icon)

        self._create_widgets()
        self._update_buttons_state()

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_add_frame()
        self._create_treeview_style()
        self._create_tree_container()
        self._create_remove_frame()

    def _create_add_frame(self):
        # Frame for adding items
        self.add_frame = tk.Frame(self, bg=Colors.ORBITAL)
        self.add_frame.grid(row=0, column=0, sticky=tk.EW, pady=10, padx=10)
        self.add_frame.grid_columnconfigure(1, weight=1)

        # Label for entry
        self.entry_label = ttk.Label(self.add_frame, text=f"Add {self.item_type}:", background=Colors.ORBITAL)
        self.entry_label.grid(row=0, column=0, padx=5)

        # Entry widget to add new items
        self.entry = tk.Entry(self.add_frame, relief=tk.SUNKEN)
        self.entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.entry.bind('<Return>', lambda event: self.add_item_from_entry())
        self.entry.bind('<KP_Enter>', lambda event: self.add_item_from_entry())
        self.entry.bind('<KeyRelease>', lambda event: self._update_add_button_state())

        # Button to add items from the entry to the treeview
        self.add_button = BlueButton(self.add_frame, text="Add", command=self.add_item_from_entry, width=6)
        self.add_button.grid(row=0, column=2, padx=5)
        self.add_button.config(state=tk.DISABLED)

    def _create_treeview_style(self):
        style = ttk.Style()

        # Treeview - Base
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25, fieldbackground=Colors.SNOWFLAKE, background=Colors.SNOWFLAKE)
        style.map('Treeview', background=[('selected', Colors.CONCRETE)], foreground=[('selected', Colors.HEART_POTION)])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': tk.NSEW})])

        # Treeview - Heading
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground=Colors.CARBON, background=Colors.BLUE_GRAY)
        style.map("Treeview.Heading", background=[('!active', Colors.BLUE_GRAY), ('active', Colors.BLUE_GRAY)], foreground=[('!active', Colors.CARBON), ('active', Colors.CARBON)])

        # Treeview - Scrollbar
        style.configure("Vertical.TScrollbar", gripcount=0, background=Colors.BLUE_GRAY, darkcolor=Colors.BLUE_GRAY, lightcolor=Colors.BLUE_GRAY, troughcolor=Colors.ORBITAL, bordercolor=Colors.BLUE_GRAY, arrowcolor=Colors.HEART_POTION)
        style.map("Vertical.TScrollbar", background=[('active', Colors.ORBITAL), ('!active', Colors.ORBITAL)], troughcolor=[('active', Colors.ORBITAL), ('!active', Colors.BLUE_GRAY)], arrowcolor=[('active', Colors.HEART_POTION), ('!active', Colors.CARBON)])

    def _create_tree_container(self):
        # Frame for the treeview and scrollbar
        self.tree_container = ttk.Frame(self, borderwidth=1, relief=tk.SUNKEN, style="Sunken.TFrame")
        self.tree_container.grid(row=1, column=0, sticky=tk.NSEW, pady=10, padx=10)
        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(0, weight=1)

        # Draggable Treeview initialized from the custom class
        self.tree = DraggableTreeview(self.tree_container, columns=(self.item_type.lower(),), show="headings")
        self.tree.heading(self.item_type.lower(), text=f"{self.item_type}s")
        self.tree.tag_configure('even', background=Colors.SNOWFLAKE)
        self.tree.tag_configure('odd', background=Colors.WHITE)
        self.tree.bind('<Delete>', lambda event: self.remove_item())
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

    def _create_remove_frame(self):
        # Frame for remove buttons
        self.remove_frame = tk.Frame(self, bg=Colors.ORBITAL)
        self.remove_frame.grid(row=2, column=0, sticky=tk.EW, pady=(5, 15), padx=10)
        self.remove_frame.grid_columnconfigure((0, 1), weight=1)

        # Button to remove all items from the treeview (left)
        self.remove_all_button = BlueButton(self.remove_frame, text="Remove All", command=self.remove_all_items, width=15)
        self.remove_all_button.grid(row=0, column=0, padx=(20, 5), pady=(0, 0), sticky=tk.EW)
        self.remove_all_button.config(state=tk.DISABLED)  # Initially disable the remove all button

        # Button to remove selected items from the treeview (right)
        self.remove_button = BlueButton(self.remove_frame, text="Remove Selected", command=self.remove_item, width=15)
        self.remove_button.grid(row=0, column=1, padx=(5, 20), pady=(0, 0), sticky=tk.EW)
        self.remove_button.config(state=tk.DISABLED)  # Initially disable the remove selected button

    def add_item_from_entry(self):
        # Add items to the treeview and clear the entry field
        item = self.entry.get()
        if item and not item.startswith('.'):
            if not messagebox.askyesno("Confirm", f"{self.item_type} '{item}' does not start with a dot. Do you want to add it anyway?", parent=self):
                return
        if item:
            self.add_item(item)
            self.entry.delete(0, "end")
            self._update_buttons_state()
            self._update_add_button_state()

    def remove_item(self):
        # Remove selected items from the treeview
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self._update_striping()
            self._update_buttons_state()

    def remove_all_items(self):
        # Confirm removal of all items
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove all {self.item_type.lower()}s?", parent=self):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self._update_striping()
            self._update_buttons_state()

    def _update_striping(self):
        # Update striping of rows after an item is removed
        for index, item in enumerate(self.tree.get_children()):
            tags = ('even',) if index % 2 == 0 else ('odd',)
            self.tree.item(item, tags=tags)

    def _update_add_button_state(self):
        if self.entry.get():
            self.add_button.config(state=tk.NORMAL)
        else:
            self.add_button.config(state=tk.DISABLED)

    def _update_buttons_state(self):
        if self.tree.get_children():
            self.remove_all_button.config(state=tk.NORMAL)
            if self.tree.selection():
                self.remove_button.config(state=tk.NORMAL)
            else:
                self.remove_button.config(state=tk.DISABLED)
        else:
            self.remove_all_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)

    def get_items(self):
        """Returns the list of items currently in the treeview."""
        return [self.tree.item(item, 'values')[0] for item in self.tree.get_children()]

    def set_items(self, items):
        """Sets the content of the treeview to the given list of items."""
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.add_item(item)

    def add_item(self, item):
        """Adds a single item to the treeview."""
        tags = ('even',) if len(self.tree.get_children()) % 2 == 0 else ('odd',)
        self.tree.insert("", tk.END, values=(item,), tags=tags)
        self._update_buttons_state()


class _DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Item Manager Demo")
        self.geometry("500x500")
        self.configure(bg=Colors.BLUE_GRAY)

        self.open_button = ttk.Button(self, text="Open Item Manager", command=self.open_item_manager)
        self.open_button.pack(pady=20)

    def open_item_manager(self):

        icon_path = str(ASSETS_DIR / "file.png")
        item_manager = ItemManager(self, item_type="Extension", icon=icon_path)
        item_manager.set_items([
            ".txt", ".pdf", ".docx", ".xlsx", ".pptx",
            ".jpg", ".png", ".gif", ".bmp", ".svg",
            ".mp3", ".wav", ".flac", ".aac", ".ogg",
            ".mp4", ".avi", ".mkv", ".mov", ".wmv",
            ".zip", ".rar", ".tar", ".gz", ".7z",
            ".html", ".css", ".js", ".json", ".xml"
        ])
        self.wait_window(item_manager)


if __name__ == '__main__':
    app = _DemoApp()
    app.mainloop()
