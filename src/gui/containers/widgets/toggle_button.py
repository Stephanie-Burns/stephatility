
import tkinter as tk
from typing import Callable, Optional

from src.gui.mixins import CallbackMixin
from src.gui.containers.widgets.tooltip import add_tooltip


class ToggleButton(CallbackMixin, tk.Canvas):
    def __init__(
            self,
            parent,
            update_callback: Optional[Callable[..., None]] = None,
            width=40,
            height=25,
            toggle_on_color='#93b373',
            toggle_off_color='#b37393',
            handle_color='#aaacaa',
            initial_state=False,
            border_color="black",
            handle_border_color="black",
            glow_color='grey',
            **kwargs
    ):
        super().__init__(
            update_callback,
            parent,
            width=width,
            height=height,
            highlightthickness=1,
            highlightbackground=border_color,
            bd=1,
            relief="solid",
            **kwargs
        )

        self.update_callback        = update_callback
        self.width                  = width
        self.height                 = height
        self.handle_size            = height - 6  # Adjust handle size to leave space above and below
        self.toggle_on_color        = toggle_on_color
        self.toggle_off_color       = toggle_off_color
        self.handle_color           = handle_color
        self.handle_border_color    = handle_border_color
        self.glow_color             = glow_color
        self.border_color           = border_color
        self._state                 = initial_state
        self.handle_outer           = None
        self.handle_inner           = None

        self._create_handle()

        self.bind("<Button-1>", self.toggle)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self._update_button()

    def on_enter(self, event):
        self.config(highlightbackground=self.glow_color)

    def on_leave(self, event):
        self.config(highlightbackground=self.border_color)

    def _create_handle(self):
        handle_margin = 3
        handle_inner_margin = 1

        # Draw the shadow part of the handle (simulating a sunken effect)
        self.handle_shadow = self.create_rectangle(
            handle_margin + 2, handle_margin + 2,
            self.handle_size + handle_margin + 2, self.handle_size + handle_margin + 2,
            fill='grey', outline=''
        )

        # Draw the outer part of the handle (black border)
        self.handle_outer = self.create_rectangle(
            handle_margin, handle_margin,
            self.handle_size + handle_margin, self.handle_size + handle_margin,
            fill=self.handle_border_color, outline=""
        )

        # Draw the highlight part of the handle (simulating a raised effect)
        self.handle_highlight = self.create_rectangle(
            handle_margin, handle_margin,
            self.handle_size + handle_margin, self.handle_size + handle_margin,
            fill='#d8d8d8', outline=''
        )

        # Draw the inner part of the handle
        self.handle_inner = self.create_rectangle(
            handle_margin + handle_inner_margin, handle_margin + handle_inner_margin,
            self.handle_size + handle_margin - handle_inner_margin,
            self.handle_size + handle_margin - handle_inner_margin,
            fill=self.handle_color, outline=""
        )

    def toggle(self, event=None):
        self._state = not self._state
        self._update_button()
        self.emit_update()


    def _update_button(self):
        # Constants for the positions
        handle_margin = 3
        handle_inner_margin = 1
        offset = ((self.height - 1) - self.handle_size) // 2  # Calculate vertical offset

        if self._state:
            self.config(bg=self.toggle_on_color)
            self.coords(
                self.handle_shadow,
                self.width - self.handle_size - handle_margin + 2, offset + handle_margin + 2,
                self.width - handle_margin + 2, self.handle_size + offset + handle_margin + 2
            )
            self.coords(
                self.handle_outer,
                self.width - self.handle_size - handle_margin, offset + handle_margin,
                self.width - handle_margin, self.handle_size + offset + handle_margin
            )
            self.coords(
                self.handle_highlight,
                self.width - self.handle_size - handle_margin, offset + handle_margin,
                self.width - handle_margin, self.handle_size + offset + handle_margin
            )
            self.coords(
                self.handle_inner,
                self.width - self.handle_size - handle_margin + handle_inner_margin, offset + handle_margin + handle_inner_margin,
                self.width - handle_margin - handle_inner_margin, self.handle_size + offset + handle_margin - handle_inner_margin
            )
        else:
            self.config(bg=self.toggle_off_color)
            self.coords(
                self.handle_shadow,
                handle_margin + 4, offset + handle_margin + 2,
                self.handle_size + handle_margin + 4, self.handle_size + offset + handle_margin + 2
            )
            self.coords(
                self.handle_outer,
                handle_margin + 2, offset + handle_margin,
                self.handle_size + handle_margin + 2, self.handle_size + offset + handle_margin
            )
            self.coords(
                self.handle_highlight,
                handle_margin + 2, offset + handle_margin,
                self.handle_size + handle_margin + 2, self.handle_size + offset + handle_margin
            )
            self.coords(
                self.handle_inner,
                handle_margin + handle_inner_margin + 2, offset + handle_margin + handle_inner_margin,
                self.handle_size + handle_margin - handle_inner_margin + 2, self.handle_size + offset + handle_margin - handle_inner_margin
            )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: bool) -> None:
        self._state = state
        self._update_button()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Toggle Button Demo")

    toggle = ToggleButton(root, initial_state=True)
    toggle.pack(pady=20)

    def print_state():
        print(f"Toggle state: {'On' if toggle.state else 'Off'}")

    state_button = tk.Button(root, text="Get Toggle State", command=print_state)
    state_button.pack(pady=20)

    root.mainloop()
