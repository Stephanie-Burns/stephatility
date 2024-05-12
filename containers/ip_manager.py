
import copy
import tkinter as tk
from typing import List


from containers.toplevel.ip_settings_modal import IPSettingsModal
from containers.frames.ip_address_field import IPV4AddressBox
from engine.ipv4_network_management import IPV4Address

class IPManager(tk.Frame):
    def __init__(self, parent: tk.Widget, current_ip: IPV4Address, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - IPManager
        self.grid(sticky='ew', padx=10, pady=10)
        self.grid_columnconfigure(0, weight=40)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.management_frame = None
        self.last_set_ipv4_address = copy.deepcopy(current_ip)

        self.label = tk.Label(self, text="IP Address:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.ip_frame = IPV4AddressBox(self, current_ip, self._update_set_button_state)
        self.ip_frame.grid(row=0, column=1, padx=(10, 20), pady=10, sticky='E')

        self.set_button = tk.Button(self, text="Apply", command=self._set_ip_address, width=20)
        self.set_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky='EW')

        self.manage_button = tk.Button(self, text="Manage", command=self._launch_manage_ip_modal, width=20)
        self.manage_button.grid(row=0, column=3, padx=10, pady=10, sticky='EW')

        self._update_set_button_state()       # Initial check



    def _update_set_button_state(self) -> None:
        if self.ip_frame.ip_address == self.last_set_ipv4_address:
            self.set_button.config(state='disabled')
        else:
            self.set_button.config(state='normal')

# ======================

    def _set_ip_address(self):
        print(f'Changing addr: {self.last_set_ipv4_address=}, to: {self.ip_frame.ip_address=}')
        self.last_set_ipv4_address = copy.deepcopy(self.ip_frame.ip_address)
        self._update_set_button_state()
        # Backend logic

    def update_ip_settings(self):
        # Optional: Callback method to handle any updates needed when management frame closes
        print("IP Settings potentially updated")

    def _launch_manage_ip_modal(self):
        print("IP Settings management invoked")

        if not self.management_frame or not self.management_frame.winfo_exists():
            self.management_frame = IPSettingsModal(self)
            self.management_frame.transient(self)
            self.management_frame.grab_set()

    def on_management_frame_close(self):
        # Properly handle the close operation
        print("Management frame has been closed")
        if self.management_frame.winfo_exists():
            self.management_frame.destroy()
        self.management_frame = None


def main():
    root = tk.Tk()
    root.title('Windows IP Manager')
    ip_manager = IPManager(root, IPV4Address.from_string("192.168.1.100"))
    ip_manager.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
