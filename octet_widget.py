import tkinter as tk
from typing import Callable, Optional, Any


class OctetWidget(tk.Entry):
    def __init__(self, master, position, initial_value="", update_callback=None):
        super().__init__(master, width=3, justify='center')
        self.position = position
        self.update_callback = update_callback
        self.previous_valid_content = initial_value if initial_value else "-1"

        self.insert(0, initial_value)
        self.vcmd = (self.register(self._validate_input), '%P', '%S', '%d')
        self.config(validate="key", validatecommand=self.vcmd)

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)

    def _validate_input(self, new_value, char, action):
        """Ensure only valid numbers are entered."""
        if action == '1':  # Key insert action
            if not char.isdigit():
                return False
            if len(new_value) > 3:
                return False
            if new_value == '0':  # Disallow '0' as a valid entry on its own
                return False
            if new_value.startswith('0') and len(new_value) > 1:  # Prevent numbers like '01', '002', etc.
                return False
            if int(new_value) > 254:
                return False
            return True
        return True  # Always allow deletion

    def _on_key_press(self, event):
        """Handle key press for special navigation and auto-advance."""
        if event.keysym in ('Return', 'KP_Enter', 'Tab'):
            self._advance_focus()
            return "break"
        elif event.keysym == 'ISO_Left_Tab':
            self._advance_focus(reverse=True)
            return "break"
        elif event.char == '.':
            self._advance_focus()
            return "break"

    def _on_key_release(self, event):
        """Check the condition on key release and advance focus if conditions are met."""
        key_is_digit = (9 < event.keycode < 20) or (78 < event.keycode < 91)
        octet_value_threshold_reached = (
                self.get() and (len(self.get()) == 3 or (len(self.get()) == 2 and int(self.get()) > 25))
        )
        if key_is_digit and octet_value_threshold_reached:
            self.after_idle(self._advance_focus)

    def _advance_focus(self, reverse=False):
        next_widget = self.tk_focusPrev() if reverse else self.tk_focusNext()
        next_widget.focus_set()

    def _on_focus_in(self, event):
        """Clear entry temporarily when gaining focus if it's not empty."""
        current_value = self.get()
        if current_value:
            self.previous_valid_content = current_value
            self.delete(0, tk.END)

    def _on_focus_out(self, event):
        """Restore previous content if no valid entry is made."""
        if not self.get():
            self.insert(0, self.previous_valid_content)

    def _on_tab_press(self, event):
        self._advance_focus()
        return "break"

    def _on_shift_tab_press(self, event):
        self._advance_focus(reverse=True)
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
            octet = OctetWidget(ip_frame, i, self.current_ip[i], update_callback=self._update_set_button_state)
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
        for octet in self.octets:
            print(f'{octet.get()=}, {octet.previous_valid_content=}')
            # will have to make this check when reading ^

def main():
    root = tk.Tk()
    ip_manager = IPManagerWidget(root, "192.168.1.100", 3)
    root.mainloop()

if __name__ == "__main__":
    main()
