import tkinter as tk

from src.application_config import logger
from src.gui.containers.toplevel.ip_settings_modal import IPSettingsModal
from src.gui.containers.frames.ip_address_field import IPV4AddressBox
from src.network_tools import NetworkService


class IPManager(tk.Frame):
    def __init__(
            self,
            parent: tk.Widget,
            network_service: NetworkService,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.modal_ip_settings = None
        self.network_service = network_service

        # Frame - IPManager
        self.grid(sticky='ew', padx=10, pady=10)
        self.grid_columnconfigure(0, weight=40)
        for i in range(3):
            self.grid_columnconfigure(i+1, weight=1)

        # Label - IP Address
        self.label = tk.Label(self, text="IP Address:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        #  Frame - IPV4 Address Box
        self.ip_frame = IPV4AddressBox(
            self,
            self.network_service.network_config.ipv4_address,
            self._check_apply_button_state
        )
        self.ip_frame.grid(row=0, column=1, padx=(10, 20), pady=10, sticky='E')

        # Button - Apply
        self.apply_button = tk.Button(self, text="Apply", command=self._set_ip_address, width=20)
        self.apply_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky='EW')

        # Button - Manage
        self.manage_button = tk.Button(self, text="Manage", command=self._launch_manage_ip_modal, width=20)
        self.manage_button.grid(row=0, column=3, padx=10, pady=10, sticky='EW')

        self._check_apply_button_state()       # Initial check

    def _check_apply_button_state(self) -> None:
        if self.network_service.network_config.has_changed():
            self.apply_button.config(state='normal')
        else:
            self.apply_button.config(state='disabled')

    def _set_ip_address(self):
        previous_address = self.network_service.network_config.previous_config.get('ipv4_address')
        current_address = self.network_service.network_config.ipv4_address
        print(f'Changing addr: {previous_address=}, to: {current_address=}')

        self.network_service.apply_configuration()
        self.network_service.network_config.reset_baseline()
        self._check_apply_button_state()

    def _callback_ip_settings_changed(self):
        self._check_apply_button_state()
        print("IP Address changed from modal")

    def _launch_manage_ip_modal(self):
        if not self.modal_ip_settings or not self.modal_ip_settings.winfo_exists():
            self.modal_ip_settings = IPSettingsModal(self, self.network_service, self._callback_ip_settings_changed)
            self.modal_ip_settings.transient(self)
            self.modal_ip_settings.grab_set()


def main():
    from src.network_tools.ipv4_addrress_configuration import IPV4AddressConfiguration
    root = tk.Tk()
    root.title('Windows IP Manager')
    ip_manager = IPManager(root, NetworkService(IPV4AddressConfiguration()))
    ip_manager.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
