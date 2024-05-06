
import tkinter as tk
from enum import StrEnum
from typing import Callable, List, Optional

from octet_widget import OctetWidget


class IPManager:
    def __init__(self, master: tk.Widget, current_ip: str, row: int):
        self.master         : tk.Widget         = master
        self.row            : int               = row
        self._octet_values  : List[str]         = current_ip.split('.')

        self.label          : tk.Label          = tk.Label(self.master, text="IP Address:")
        self.ip_frame       : tk.Frame          = tk.Frame(self.master)
        self.octets         : List[OctetWidget] = []
        self.set_button     : tk.Button         = tk.Button(self.master, text="Set", command=self._set_ip_address)
        self.manage_button  : tk.Button         = tk.Button(self.master, text="Manage", command=self._manage_ip_settings)
        self.setup()

    def setup(self):

        self.label.grid(row=self.row, column=1, padx=10, pady=10, sticky='w')
        self.ip_frame.grid(row=self.row, column=1, padx=10, pady=10, sticky='e')

        for i in range(4):
            octet = OctetWidget(
                self.ip_frame,
                i,
                initial_value=self._octet_values[i],
                update_callback=self._update_set_button_state
            )
            octet.bind("<FocusOut>", lambda event, idx=i: self.octet_focus_out(event, idx))
            octet.pack(side=tk.LEFT)

            if i < 3:
                tk.Label(self.ip_frame, text=".").pack(side=tk.LEFT, padx=3)

            self.octets.append(octet)

        self.set_button.grid(row=self.row, column=2, padx=10, pady=10, sticky='EW')
        self.manage_button.grid(row=self.row, column=3, padx=10, pady=10, sticky='EW')

        self._update_set_button_state()             # Initial check

    def octet_focus_out(self, event, idx):
        """Handle focus out for each octet and update the 'Set' button state."""
        octet = self.octets[idx]

        if not octet.get():                         # Restore the previous value if an octet unset
            octet.insert(0, octet.previous_valid_content)

        self._update_set_button_state()

        if octet.focus_travel_direction == 1:       # Forwards
            octet.tk_focusNext().focus_set()
        elif octet.focus_travel_direction == -1:    # Backwards
            octet.tk_focusPrev().focus_set()

    def _update_set_button_state(self) -> None:

        octets = [octet.get() for octet in self.octets]

        if octets == self._octet_values:
            self.set_button.config(state='disabled')
        elif not all(octets):
            self.set_button.config(state='disabled')
        else:
            self.set_button.config(state='normal')


# ======================
    @property
    def get_current_ip(self) -> str:
        return ".".join(octet.get() for octet in self.octets)

    def _set_ip_address(self):
        ip = self._octet_values
        print(f"IP Address set to: {ip}")

    def _manage_ip_settings(self):
        print("IP Settings management invoked")
        for octet in self.octets:
            print(f'{octet.get()=}, {octet.previous_valid_content=}')
            # will have to make this check when reading ^

    def _backend_ip_change(self):
        print("Passing to script...")
        print("Backend IP Changed")

    def _backend_ip_read(self):
        print("Passing to Windows IP Manager...")
        print("Backend IP is...")


def main():
    root = tk.Tk()
    ip_manager = IPManager(root, "192.168.1.100", 3)
    root.mainloop()

if __name__ == "__main__":
    main()
