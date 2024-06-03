
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from typing import Callable, List, Optional, Tuple, Union

from src.constants import Colors
from src.gui.containers.widgets.draggable_treeview import DraggableTreeview
from src.gui.containers.widgets.blue_button import BlueButton
from src.gui.icon_manager import IconManager
from src.gui.mixins import CallbackMixin


class BaseItemManager(tk.Frame):
    def __init__(
            self,
            parent          : tk.Widget,
            uid             : int = 0,
            item_type       : str = "Item",
            items           : List[str] | List[Tuple[str, ...]] = None,
            column_names: Optional[List[str]] = None,
            update_callback : Optional[Callable[..., None]] = None,
            **kwargs
    ):
        super().__init__(parent, borderwidth=2, relief="raised", bg=Colors.ORBITAL, **kwargs)
        self.uid = uid
        self.item_type = item_type
        self.initial_items = items
        self.column_names = column_names or [self.item_type]

        self._create_widgets()
        self.set_items(self.initial_items)
        self._update_buttons_state()

    def add_item_from_entry(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def _create_add_frame(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def _get_columns(self) -> List[Tuple[str, str]]:
        return [(name, name) for name in self.column_names]

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_add_frame()
        self._create_treeview_style()
        self._create_tree_container()
        self._create_remove_frame()

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
        self.tree = DraggableTreeview(self.tree_container, columns=[col[0] for col in self._get_columns()], show="headings")
        for col, heading in self._get_columns():
            self.tree.heading(col, text=heading)
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

    def _update_striping(self):
        # Update striping of rows after an item is removed
        for index, item in enumerate(self.tree.get_children()):
            tags = ('even',) if index % 2 == 0 else ('odd',)
            self.tree.item(item, tags=tags)

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

    def get_items(self) -> Union[List[str], List[Tuple[str, ...]]]:
        """Returns the list of items currently in the treeview."""
        items = [self.tree.item(item, 'values') for item in self.tree.get_children()]
        if len(self.tree["columns"]) == 1:
            return [item[0] for item in items]  # Return a list of strings if there's only one column
        else:
            return [tuple(item) for item in items]  # Return a list of tuples if there are multiple columns

    def set_items(self, items: Union[list[str], List[Tuple[str, ...]]]):
        """Sets the content of the treeview to the given list of items."""
        self.tree.delete(*self.tree.get_children())
        for item in items:
            if isinstance(item, tuple):
                self.add_item(*item)
            else:
                self.add_item(item)

    def add_item(self, *items):
        """Adds a single item to the treeview."""
        tags = ('even',) if len(self.tree.get_children()) % 2 == 0 else ('odd',)
        self.tree.insert("", tk.END, values=items, tags=tags)
        self._update_buttons_state()


class ToplevelBase(CallbackMixin, tk.Toplevel):
    def __init__(
            self,
            parent: Optional[tk.Misc] = None,
            icon: Optional[PhotoImage] = None,
            update_callback: Optional[Callable[..., None]] = None,
            **kwargs
    ):
        super().__init__(update_callback, parent, **kwargs)
        self.attributes("-topmost", True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.icon = icon
        self.icon_manager = IconManager()

        if self.icon:
            self.iconphoto(False, self.icon)
        else:
            self.iconphoto(False, self.icon_manager.get_icon('item', (16, 16)))

    def _on_close(self):
        self.grab_release()
        self.emit_update()
        self.destroy()


class SingleColumnItemManagerTopLevel(ToplevelBase):
    def __init__(
            self,
            update_callback : Optional[Callable[..., None]] = None,
            parent          : Optional[tk.Misc] = None,
            icon            : Optional[PhotoImage] = None,
            uid             : Optional[int] = 0,
            item_type       : Optional[str] = 'Item',
            items           : Optional[Union[List[str], List[Tuple[str, ...]]]] = None,
            column_names    : Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(update_callback=update_callback, parent=parent, icon=icon, **kwargs)
        self.title(f"{item_type} Manager")
        self.geometry("400x500")
        self.resizable(True, True)

        self.item_manager_frame = ttk.Frame(self)
        self.item_manager_frame.pack(expand=True, fill=tk.BOTH)

        self.item_manager = SingleColumnItemManager(
            parent=self.item_manager_frame,
            uid=uid, items=items,
            item_type=item_type,
            column_names=column_names,
            update_callback=update_callback
        )
        self.item_manager.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class DoubleColumnItemManagerTopLevel(ToplevelBase):
    def __init__(
            self,
            update_callback : Optional[Callable[..., None]] = None,
            parent          : Optional[tk.Misc] = None,
            icon            : Optional[PhotoImage] = None,
            uid             : Optional[int] = 0,
            item_type       : Optional[str] = 'Item',
            items           : Optional[Union[List[str], List[Tuple[str, ...]]]] = None,
            column_names    : Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(update_callback=update_callback, parent=parent, icon=icon, **kwargs)
        self.title(f"{item_type} Manager")
        self.geometry("400x500")
        self.resizable(True, True)

        self.item_manager_frame = ttk.Frame(self)
        self.item_manager_frame.pack(expand=True, fill=tk.BOTH)

        self.item_manager = DoubleColumnItemManager(
            parent=self.item_manager_frame,
            uid=uid,
            items=items,
            item_type=item_type,
            column_names=column_names,
            update_callback=update_callback
        )
        self.item_manager.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class _DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Item Manager Demo")
        self.geometry("600x600")
        self.configure(bg=Colors.BLUE_GRAY)

        configure_styles()
        initialize_icons()

        config_double = [("Item1A", "Item1B"), ("Item2A", "Item2B"), ("Item3A", "Item3B")]

        config_single = [".txt", ".pdf", ".docx"]

        self.open_single_button = ttk.Button(
            self, text="Open Single Column Manager", command=lambda: self.open_single_column_manager(config_single)
        )
        self.open_single_button.pack(pady=10)

        self.open_two_button = ttk.Button(
            self, text="Open Two Column Manager", command=lambda: self.open_two_column_manager(config_double)
        )
        self.open_two_button.pack(pady=10)

    def open_single_column_manager(self, user_settings):

        item_manager = SingleColumnItemManagerTopLevel(
            parent=self, uid=0, items=user_settings, item_type="Item", column_names=["Extensions"]
        )

        self.wait_window(item_manager)

    def open_two_column_manager(self, user_settings):

        icon_manager = IconManager()
        icon = icon_manager.get_icon('vault', (16, 16))

        # TODO column_names = ['Source', 'Password']
        item_manager = DoubleColumnItemManagerTopLevel(
            parent=self, items=user_settings, item_type="Password", icon=icon, column_names=["Source", "Password"]
        )

        self.wait_window(item_manager)


if __name__ == '__main__':
    from src.gui.styles import configure_styles
    from src.application_config.icon_setup import initialize_icons
    from src.gui.containers.toplevel.single_column_item_manager import SingleColumnItemManager
    from src.gui.containers.toplevel.double_column_item_manager import DoubleColumnItemManager

    app = _DemoApp()
    app.mainloop()
