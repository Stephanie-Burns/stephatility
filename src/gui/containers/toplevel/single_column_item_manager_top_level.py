
import tkinter as tk
from tkinter import ttk, PhotoImage
from typing import Callable, List, Optional, Tuple, Union

from src.gui.containers.toplevel.base.top_level_base import ToplevelBase
from src.gui.containers.widgets.single_column_item_manager import SingleColumnItemManager


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
        self.resizable(True, True)

        self.item_manager_frame = ttk.Frame(self)
        self.item_manager_frame.pack(expand=True, fill=tk.BOTH)

        self.item_manager = SingleColumnItemManager(
            parent=self.item_manager_frame,
            uid=uid,
            items=items,
            item_type=item_type,
            column_names=column_names,
            update_callback=update_callback
        )
        self.item_manager.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
