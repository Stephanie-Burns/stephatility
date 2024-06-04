
import tkinter as tk
from tkinter import PhotoImage
from typing import Callable, Optional

from src.gui.icon_manager import IconManager
from src.gui.mixins import CallbackMixin


class ToplevelBase(CallbackMixin, tk.Toplevel):
    def __init__(
            self,
            parent: Optional[tk.Misc] = None,
            icon: Optional[PhotoImage] = None,
            update_callback: Optional[Callable[..., None]] = None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)
        self.update_callback = update_callback
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
