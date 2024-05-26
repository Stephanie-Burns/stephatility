
import tkinter as tk
import tkinter.ttk as ttk
from typing import List, Tuple

from src.constants import Colors
from src.gui.containers.toplevel.base.base_item_manager import BaseItemManager


class DoubleColumnItemManager(BaseItemManager):
    def _create_add_frame(self):
        # Frame for adding items
        self.add_frame = tk.Frame(self, bg=Colors.ORBITAL)
        self.add_frame.grid(row=0, column=0, sticky=tk.EW, pady=10, padx=10)
        self.add_frame.grid_columnconfigure(3, weight=1)

        # Label for entry 1
        self.entry_label1 = ttk.Label(self.add_frame, text=f"Add {self.item_type} 1:", background=Colors.ORBITAL)
        self.entry_label1.grid(row=0, column=0, padx=5)

        # Entry widget 1 to add new items
        self.entry1 = tk.Entry(self.add_frame, relief=tk.SUNKEN)
        self.entry1.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.entry1.bind('<Return>', lambda event: self.add_item_from_entry())
        self.entry1.bind('<KP_Enter>', lambda event: self.add_item_from_entry())
        self.entry1.bind('<KeyRelease>', lambda event: self._update_add_button_state())

        # Label for entry 2
        self.entry_label2 = ttk.Label(self.add_frame, text=f"Add {self.item_type} 2:", background=Colors.ORBITAL)
        self.entry_label2.grid(row=1, column=0, padx=5)

        # Entry widget 2 to add new items
        self.entry2 = tk.Entry(self.add_frame, relief=tk.SUNKEN)
        self.entry2.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.entry2.bind('<Return>', lambda event: self.add_item_from_entry())
        self.entry2.bind('<KP_Enter>', lambda event: self.add_item_from_entry())
        self.entry2.bind('<KeyRelease>', lambda event: self._update_add_button_state())

        # Button to add items from the entry to the treeview
        self.add_button = ttk.Button(
            self.add_frame,
            text="Add",
            style="Blue.TButton",
            width=6,
            command=self.add_item_from_entry,
        )
        self.add_button.grid(row=0, column=2, rowspan=2, padx=5)
        self.add_button.state(['disabled'])

    def _get_columns(self) -> List[Tuple[str, str]]:
        return [
            (f"{self.item_type.lower()}1", f"{self.item_type} 1"),
            (f"{self.item_type.lower()}2", f"{self.item_type} 2")
        ]

    def add_item_from_entry(self):
        # Add items to the treeview and clear the entry fields
        item1 = self.entry1.get()
        item2 = self.entry2.get()
        if item1 and item2:
            self.add_item(item1, item2)
            self.entry1.delete(0, "end")
            self.entry2.delete(0, "end")
            self._update_buttons_state()
            self._update_add_button_state()

    def _update_add_button_state(self):
        if self.entry1.get() and self.entry2.get():
            self.add_button.state(['!disabled'])
        else:
            self.add_button.state(['disabled'])
