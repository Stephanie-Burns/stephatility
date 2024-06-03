
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Tuple

from src.constants import Colors
from src.gui.containers.toplevel.base.base_item_manager import BaseItemManager

from src.gui.containers.widgets.blue_button import BlueButton


class SingleColumnItemManager(BaseItemManager):
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

    def _get_columns(self) -> List[Tuple[str, str]]:
        return [(self.item_type.lower(), self.column_names[0])]

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

    def _update_add_button_state(self):
        if self.entry.get():
            self.add_button.config(state=tk.NORMAL)
        else:
            self.add_button.config(state=tk.DISABLED)
