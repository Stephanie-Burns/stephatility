import tkinter as tk


class OctetWidget(tk.Entry):
    def __init__(self, master, on_advance_focus, position, initial_value="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_advance_focus = on_advance_focus
        self.position = position
        self.insert(0, initial_value)
        self.config(width=3, justify='center')

        vcmd = (master.register(self.validate_input), '%S', '%d')
        self.config(validate='key', validatecommand=vcmd)

        self.bind('<FocusOut>', self.on_focus_out)
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<Button-1>', self.on_mouse_click)
        self.previous_valid_content = initial_value  # Keep track of last valid input

    def validate_input(self, char, action):
        if action == '1':  # action 1 is insert
            if char.isdigit():
                return True
            elif char == '.':
                self.tk_focusNext().focus()
                return False
        elif action == '0':  # action 0 is delete
            return True
        return False

    def on_key_press(self, event):
        # Handle normal Enter or KP_Enter (moving forward)
        if event.keysym in ['Return', 'KP_Enter'] and not (event.state & 0x0001):  # No Shift key
            next_widget = self.tk_focusNext()
            next_widget.focus_set()
            if isinstance(next_widget, tk.Entry):
                next_widget.icursor(0)
            return "break"

        # Handle Shift+Enter or Shift+KP_Enter (moving backward)
        elif event.keysym in ['Return', 'KP_Enter'] and (event.state & 0x0001):  # Shift key held
            if self.position == 0:  # Check if it's the first octet
                return "break"  # Prevent moving out of the first octet
            prev_widget = self.tk_focusPrev()
            prev_widget.focus_set()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.icursor(len(prev_widget.get()))
            return "break"

        # Handle Tab and Shift+Tab for navigation
        elif event.keysym == 'Tab' and not (event.state & 0x0001):
            next_widget = self.tk_focusNext()
            next_widget.focus_set()
            if isinstance(next_widget, tk.Entry):
                next_widget.icursor(0)
            return "break"
        elif event.keysym == 'ISO_Left_Tab':
            prev_widget = self.tk_focusPrev()
            prev_widget.focus_set()
            if isinstance(prev_widget, tk.Entry):
                prev_widget.icursor(len(prev_widget.get()))
            return "break"

        # Handle Backspace for deleting and moving backwards
        elif event.keysym == 'BackSpace':
            if self.position == 0 and not self.get():
                return "break"
            elif self.index('insert') == 0:
                prev_widget = self.tk_focusPrev()
                if isinstance(prev_widget, tk.Entry):
                    prev_widget.focus_set()
                    prev_widget.icursor(len(prev_widget.get()))
                return "break"

        # Handle Delete for deleting forward
        elif event.keysym == 'Delete':
            current_text = self.get()
            cursor_pos = self.index('insert')
            if cursor_pos < len(current_text):
                self.delete(cursor_pos, cursor_pos + 1)
            if cursor_pos == len(current_text) and self.position != 3:
                next_widget = self.tk_focusNext()
                if isinstance(next_widget, tk.Entry):
                    next_widget.focus_set()
                    next_widget.icursor(0)
            return "break"

        # Handle arrow keys for intra-widget navigation
        elif event.keysym == 'Left':
            if self.index('insert') == 0:
                prev_widget = self.tk_focusPrev()
                if isinstance(prev_widget, tk.Entry):
                    prev_widget.focus_set()
                    prev_widget.icursor(len(prev_widget.get()))
                return "break"
        elif event.keysym == 'Right':
            if self.index('insert') == len(self.get()):
                next_widget = self.tk_focusNext()
                if isinstance(next_widget, tk.Entry):
                    next_widget.focus_set()
                    next_widget.icursor(0)
                return "break"

        return "continue"

    def on_focus_out(self, event):
        if not self.get().isdigit() or not (1 <= int(self.get()) <= 254):
            self.delete(0, tk.END)
            self.insert(0, self.previous_valid_content if hasattr(self, 'previous_valid_content') else "")

    def on_mouse_click(self, event):
        self.select_range(0, tk.END)  # Select all text on click to ease replacement


class IPManagerWidget:
    def __init__(self, master, row, current_ip):
        self.master = master
        self.row = row
        self.current_ip = current_ip.split('.')
        self.setup()

    def setup(self):
        ip_frame = tk.Frame(self.master)
        tk.Label(self.master, text="IP Address:").grid(row=self.row, column=0, padx=10, pady=10, sticky='w')
        ip_frame.grid(row=self.row, column=1, padx=10, pady=10, sticky='ew')  # Ensure it uses full width available

        self.octets = []
        for i in range(4):
            octet = OctetWidget(ip_frame, self.advance_focus, i, self.current_ip[i])
            octet.pack(side=tk.LEFT, expand=True, fill='both')  # Ensure filling in horizontal space
            if i < 3:
                tk.Label(ip_frame, text=".").pack(side=tk.LEFT)
            self.octets.append(octet)
            print(f"Octet {i} initialized with value {self.current_ip[i]}")  # Print to check values

        self.set_button = tk.Button(self.master, text="Set", command=self.set_ip_address)
        self.set_button.grid(row=self.row, column=2, padx=10, pady=10, sticky='EW')
        manage_button = tk.Button(self.master, text="Manage", command=self.manage_ip_settings)
        manage_button.grid(row=self.row, column=3, padx=10, pady=10, sticky='EW')

        print(f"Total octets packed: {len(self.octets)}")  # Verify all octets are packed

    def advance_focus(self, index):
        # Logic to advance focus to the next widget
        pass

    def set_ip_address(self):
        ip_address = ".".join(octet.get() for octet in self.octets)
        # Add logic to verify IP address uniqueness and availability here
        print(f"IP Address set to: {ip_address}")

    def manage_ip_settings(self):
        print("IP Settings management invoked")

# Example app setup
def main():
    root = tk.Tk()
    ip_manager = IPManagerWidget(root, 3, "192.168.1.100")
    root.mainloop()

if __name__ == "__main__":
    main()
