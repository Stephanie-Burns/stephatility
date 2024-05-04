import tkinter as tk
from typing import Callable, Optional, Any

class OctetWidget(tk.Entry):
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
                # Advance to the next widget and prevent the '.' from being inserted
                self.after_idle(self._advance_focus)
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

    def _advance_focus(self):
        """Advance the focus to the next widget, typically the next octet entry or the Set button."""
        next_widget = self.tk_focusNext()
        if isinstance(next_widget, tk.Entry) or (self.position == 3 and isinstance(next_widget, tk.Button)):
            next_widget.focus_set()
            if isinstance(next_widget, tk.Entry):
                next_widget.icursor(0)

    def _on_mouse_click(self, event: tk.Event):
        print("Mouse click event detected.")  # Debug output
        self.previous_valid_content = self.get()  # Save the current value before clearing
        self.delete(0, tk.END)  # Clear the field to allow easy new input
        print(f"Stored value on click: {self.previous_valid_content}")

    def _on_focus_out(self, event: tk.Event):
        print("Focus out event detected.")
        current_value = self.get()
        if not current_value:  # If the field is empty after focus is lost
            self.insert(0, self.previous_valid_content)  # Restore the previously stored value
        elif not current_value.isdigit() or not (1 <= int(current_value) <= 254):
            self.delete(0, tk.END)
            self.insert(0, self.previous_valid_content)  # Restore if the new input is invalid
        if self.update_callback:
            self.update_callback()

    def _on_key_press(self, event: tk.Event) -> str:
        key_handlers = {
            'Return': self._handle_enter,
            'KP_Enter': self._handle_enter,
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

    def _handle_enter(self, event: tk.Event) -> str:
        if not (event.state & 0x0001):  # No Shift key
            next_widget = self.tk_focusNext()
            next_widget.focus_set()
            if isinstance(next_widget, tk.Entry):
                next_widget.icursor(0)
            self.update_callback()
            return "break"
        else:  # Shift key held
            if self.position == 0:
                return "break"
            prev_widget = self.tk_focusPrev()
            prev_widget.focus_set()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.icursor(len(prev_widget.get()))
            self.update_callback()
            return "break"

    def _handle_tab(self, event: tk.Event) -> str:
        next_widget = self.tk_focusNext()
        next_widget.focus_set()
        if isinstance(next_widget, tk.Entry):
            next_widget.icursor(0)
        self.update_callback()
        return "break"

    def _handle_shift_tab(self, event: tk.Event) -> str:
        prev_widget = self.tk_focusPrev()
        prev_widget.focus_set()
        if isinstance(prev_widget, tk.Entry):
            prev_widget.icursor(len(prev_widget.get()))
        self.update_callback()
        return "break"

    def _handle_backspace(self, event: tk.Event) -> str:
        if self.position == 0 and not self.get():
            return "break"
        elif self.index('insert') == 0:
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))
            self.update_callback()
            return "break"

    def _handle_delete(self, event: tk.Event) -> str:
        current_text = self.get()
        cursor_pos = self.index('insert')
        if cursor_pos < len(current_text):
            self.delete(cursor_pos, cursor_pos + 1)
        if cursor_pos == len(current_text) and self.position != 3:
            next_widget = self.tk_focusNext()
            if isinstance(next_widget, tk.Entry):
                next_widget.focus_set()
                next_widget.icursor(0)
        self.update_callback()
        return "break"

    def _handle_left_arrow(self, event: tk.Event) -> str:
        if self.index('insert') == 0:
            prev_widget = self.tk_focusPrev()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.focus_set()
                prev_widget.icursor(len(prev_widget.get()))
            self.update_callback()
            return "break"

    def _handle_right_arrow(self, event: tk.Event) -> str:
        if self.index('insert') == len(self.get()):
            next_widget = self.tk_focusNext()
            if isinstance(next_widget, tk.Entry):
                next_widget.focus_set()
                next_widget.icursor(0)
            self.update_callback()
            return "break"


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
