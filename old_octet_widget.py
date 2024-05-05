import tkinter as tk
from typing import Callable, Optional, Any

class OctetWidgfet(tk.Entry):
    def __init__(
            self,
            master                  : tk.Widget,
            on_advance_focus        : Callable,
            position                : int,
            initial_value           : str = "",
            update_callback         : Optional[Callable] = None,
            *args                   : Any,
            **kwargs                : Any
    ):
        super().__init__(master, *args, **kwargs)
        self.on_advance_focus       : Callable[[int], None] = on_advance_focus
        self.position               : int = position
        self.update_callback        : Optional[Callable[[], None]] = update_callback
        self.previous_valid_content : str = initial_value

        self.insert(0, initial_value)
        self.config(width=3, justify='center')

        vcmd = (master.register(self._validate_input), '%P', '%S', '%d')
        self.config(validate='key', validatecommand=vcmd)

        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<KeyPress>', self._on_key_press)
        self.bind('<Button-1>', self._on_mouse_click)

    def _validate_input(self, new_value: str, char: str, action: str) -> bool:
        if action == '1':  # Insert action
            if char == '.':
                # Advance to the next widget but do not clear the current widget if not necessary
                self.after_idle(lambda: self._advance_focus(clear_field=False))  # Ensure not to clear field on '.'
                return False
            if not char.isdigit():
                return False
            if len(new_value) > 3:
                return False
            if new_value and 1 <= int(new_value) <= 254:
                return True
            # Temporarily allow entering initial digits
            if new_value in ('0', '25'):
                return True
        elif action == '0':  # Delete action
            return True
        return False

    def _advance_focus(self, backward=False, clear_field=True):
        """Advance the focus to the next widget, handling fields and buttons appropriately."""
        if clear_field:
            self.previous_valid_content = self.get()
            self.delete(0, tk.END)

        widget = self.tk_focusPrev() if backward else self.tk_focusNext()

        if isinstance(widget, tk.Entry):
            widget.focus_set()
            widget.icursor(0)
        elif isinstance(widget, tk.Button) and not backward:
            # Only focus the button if advancing forward; do not attempt to place the cursor
            widget.focus_set()

        self.invoke_update_callback()

    def _clear_and_focus(self, clear: bool, backward: bool = False):
        if clear:
            self.previous_valid_content = self.get()
            self.delete(0, tk.END)
        if backward:
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))
        else:
            next_widget = self.tk_focusNext()
            if isinstance(next_widget, tk.Entry):
                next_widget.focus_set()
                next_widget.icursor(0)

    def _on_mouse_click(self, event: tk.Event):
        self._clear_and_focus(True)

    def _on_focus_out(self, event: tk.Event):
        current_value = self.get()
        if not current_value:
            self.insert(0, self.previous_valid_content)
        elif not current_value.isdigit() or not (1 <= int(current_value) <= 254):
            self.delete(0, tk.END)
            self.insert(0, self.previous_valid_content)

        self.invoke_update_callback()

    def _on_key_press(self, event: tk.Event) -> str:
        """Handle key press with specific actions for different keys."""
        key_handlers = {
            'Return': lambda e: self._handle_enter(e),
            'KP_Enter': lambda e: self._handle_enter(e),
            'Tab': self._handle_tab,
            'ISO_Left_Tab': self._handle_shift_tab,
            'BackSpace': self._handle_backspace,
            'Delete': self._handle_delete,
            'Left': self._handle_left_arrow,
            'Right': self._handle_right_arrow
        }
        handler = key_handlers.get(event.keysym)
        if handler:
            return handler(event)
        return "continue"

    def _handle_backspace(self, event: tk.Event) -> str:
        if self.get() == "" and self.position == 0:
            # If the first octet is empty and backspace is pressed, do nothing
            return "break"
        elif self.index('insert') == 0:
            # If the cursor is at the start of the octet, move focus backward
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))  # Position cursor at the end
            self.invoke_update_callback()
            return "break"
        return "continue"  # Allow normal backspace operation

    def _handle_delete(self, event: tk.Event) -> str:
        current_text = self.get()
        cursor_pos = self.index('insert')
        if cursor_pos < len(current_text):
            self.delete(cursor_pos, cursor_pos + 1)
        elif cursor_pos == len(current_text) and self.position != 3:
            # If at the end of the octet and not the last one, move forward without clearing
            self._advance_focus(clear_field=False)
        self.invoke_update_callback()
        return "break"

    def _handle_enter(self, event: tk.Event) -> str:
        """Handle Enter and KP_Enter keys, considering the Shift modifier."""
        if not (event.state & 0x0001):  # No Shift key
            if self.get() == "":
                # If the octet is empty, restore previous content
                self.insert(0, self.previous_valid_content)
            self._clear_and_focus(clear=False)  # Move focus without clearing
            self.invoke_update_callback()
            return "break"
        else:  # Shift key held
            if self.position == 0:
                # Prevent leaving the first octet and ensure cursor is at the start
                self.focus_set()
                self.icursor(0)  # Set cursor at the start of the octet
                return "break"
            # Move focus to the previous widget and place the cursor at the end of its content
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))
            self.invoke_update_callback()
            return "break"

    def _handle_left_arrow(self, event: tk.Event) -> str:
        if self.index('insert') == 0:
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))
            self.invoke_update_callback()
            return "break"

    def _handle_right_arrow(self, event: tk.Event) -> str:
        if self.index('insert') == len(self.get()):
            next_widget = self.tk_focusNext()
            if isinstance(next_widget, tk.Entry):
                next_widget.focus_set()
                next_widget.icursor(0)
            self.invoke_update_callback()
            return "break"

    def _handle_tab(self, event: tk.Event) -> str:
        """Handle Tab key, advancing focus forward and restoring content if necessary."""
        if self.get() == "":
            # If the octet is empty, restore the previous valid content
            self.insert(0, self.previous_valid_content)
        self._advance_focus(clear_field=False)  # Move focus to the next widget without clearing
        self.invoke_update_callback()
        return "break"

    def _handle_shift_tab(self, event: tk.Event) -> str:
        """Handle Shift+Tab key, moving focus backward and allowing exit from the first octet."""
        if self.position == 0:  # If it's the first octet, allow the focus to move out
            prev_widget = self.tk_focusPrev()
            if prev_widget:  # Ensure there is a widget to focus on
                prev_widget.focus_set()
                if isinstance(prev_widget, tk.Entry):
                    prev_widget.icursor(len(prev_widget.get()))  # Place cursor at the end
            self.invoke_update_callback()
            return "break"
        # For other octets, handle as usual
        prev_widget = self.tk_focusPrev()
        prev_widget.focus_set()
        if isinstance(prev_widget, tk.Entry):
            prev_widget.icursor(len(prev_widget.get()))  # Place cursor at the end
        self.invoke_update_callback()
        return "break"

    def invoke_update_callback(self):
        """Safely invoke the update callback if it exists."""
        if self.update_callback:
            self.update_callback()


class IPManagerWidget:
    def __init__(self, master: tk.Widget, current_ip: str, row: int):
        self.master = master
        self.row = row
        self.current_ip = current_ip.split('.')
        self.setup()

    def setup(self):
        ip_frame = tk.Frame(self.master)
        tk.Label(self.master, text="IP Address:").grid(row=self.row, column=1, padx=10, pady=10, sticky='w')
        ip_frame.grid(row=self.row, column=1, padx=10, pady=10, sticky='e')

        self.octets = []
        for i in range(4):
            octet = OctetWidget(ip_frame, self._advance_focus, i, self.current_ip[i], update_callback=self._update_set_button_state)
            octet.pack(side=tk.LEFT, expand=True, fill='both')
            if i < 3:
                tk.Label(ip_frame, text=".").pack(side=tk.LEFT)
            self.octets.append(octet)

        self.set_button = tk.Button(self.master, text="Set", command=self._set_ip_address)
        self.set_button.grid(row=self.row, column=2, padx=10, pady=10, sticky='EW')
        manage_button = tk.Button(self.master, text="Manage", command=self._manage_ip_settings)
        manage_button.grid(row=self.row, column=3, padx=10, pady=10, sticky='EW')

        self._update_set_button_state()  # Initial check

    def _update_set_button_state(self):
        current_ip = ".".join(octet.get() for octet in self.octets)
        if current_ip == ".".join(self.current_ip):
            self.set_button.config(state='disabled')
        else:
            self.set_button.config(state='normal')

    def _advance_focus(self, index: int):
        # Logic to advance focus to the next widget
        pass

    def _set_ip_address(self):
        ip_address = ".".join(octet.get() for octet in self.octets)
        print(f"IP Address set to: {ip_address}")

    def _manage_ip_settings(self):
        print("IP Settings management invoked")


def main():
    root = tk.Tk()
    ip_manager = IPManagerWidget(root, "192.168.1.100", 3)
    root.mainloop()


if __name__ == "__main__":
    main()
