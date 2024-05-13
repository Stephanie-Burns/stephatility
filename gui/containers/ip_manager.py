
import copy
import tkinter as tk

from gui.containers.toplevel.ip_settings_modal import IPSettingsModal
from gui.containers.frames.ip_address_field import IPV4AddressBox
from network_tools.ipv4_address import IPV4Address

class IPManager(tk.Frame):
    def __init__(self, parent: tk.Widget, current_ip: IPV4Address, network_service, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - IPManager
        self.grid(sticky='ew', padx=10, pady=10)
        self.grid_columnconfigure(0, weight=40)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.management_frame = None
        self.last_set_ipv4_address = copy.deepcopy(current_ip)
        self.current_ip = current_ip
        self.network_service = network_service
        self.network_config = None  # TODO get from service later

        self.label = tk.Label(self, text="IP Address:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.ip_frame = IPV4AddressBox(self, current_ip, self._check_apply_button_state)
        self.ip_frame.grid(row=0, column=1, padx=(10, 20), pady=10, sticky='E')

        self.set_button = tk.Button(self, text="Apply", command=self._set_ip_address, width=20)
        self.set_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky='EW')

        self.manage_button = tk.Button(self, text="Manage", command=self._launch_manage_ip_modal, width=20)
        self.manage_button.grid(row=0, column=3, padx=10, pady=10, sticky='EW')

        self._check_apply_button_state()       # Initial check



    def _check_apply_button_state(self) -> None:
        if self.ip_frame.ip_address == self.last_set_ipv4_address:
            self.set_button.config(state='disabled')
        else:
            self.set_button.config(state='normal')

# ======================

    def _set_ip_address(self):
        print(f'Changing addr: {self.last_set_ipv4_address=}, to: {self.ip_frame.ip_address=}')
        self.last_set_ipv4_address = copy.deepcopy(self.ip_frame.ip_address)
        self._check_apply_button_state()

        # Backend logic
        # set with defaults if config is blank
        self.network_service.apply_configuration(self.network_config)

    def _callback_ip_settings_changed(self):

        self.last_set_ipv4_address = copy.deepcopy(self.current_ip)
        self._check_apply_button_state()

        print("IP Settings potentially updated")

    def _launch_manage_ip_modal(self):
        print("IP Settings management invoked")

        if not self.management_frame or not self.management_frame.winfo_exists():
            self.management_frame = IPSettingsModal(self, self._callback_ip_settings_changed)
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
