import tkinter as tk

from src.application_config.logger import app_logger
from src.gui.containers.frames import IPV4AddressBox
from src.gui.containers.toplevel import IPSettingsModal
from src.engine.network_tools import NetworkService


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
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        #  Frame - IPV4 Address Box
        self.ip_frame = IPV4AddressBox(
            self,
            self.network_service.network_config.ipv4_address,
            self._check_apply_button_state
        )
        self.ip_frame.grid(row=0, column=1, padx=(10, 20), pady=10, sticky=tk.E)

        # Button - Apply
        self.apply_button = tk.Button(self, text="Apply", command=self._set_ip_address, width=20)
        self.apply_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky=tk.EW)
        self.apply_button.bind('<Return>', self._on_enter)
        self.apply_button.bind('<KP_Enter>', self._on_enter)

        # Button - Manage
        self.manage_button = tk.Button(self, text="Manage", command=self._launch_manage_ip_modal, width=20)
        self.manage_button.grid(row=0, column=3, padx=10, pady=10, sticky=tk.EW)

        self._check_apply_button_state()       # Initial check

    def _check_apply_button_state(self) -> None:
        if self.network_service.network_config.has_changed():
            self.apply_button.config(state='normal')
        else:
            self.apply_button.config(state='disabled')

    def _set_ip_address(self):
        app_logger.info(
            "Changing IP from %s, to: %s",
            self.network_service.network_config.previous_config.get('ipv4_address'),
            self.network_service.network_config.ipv4_address
        )

        self.network_service.apply_configuration()
        self.network_service.network_config.reset_baseline()
        self._check_apply_button_state()

    def _on_enter(self, event):
        if self.apply_button == self.focus_get():
            self.apply_button.invoke()

    def _launch_manage_ip_modal(self):
        if not self.modal_ip_settings or not self.modal_ip_settings.winfo_exists():
            self.modal_ip_settings = IPSettingsModal(self, self.network_service, self._on_modal_ip_change)
            self.modal_ip_settings.transient(self)
            self.modal_ip_settings.grab_set()

    def _on_modal_ip_change(self):
        self._check_apply_button_state()
        self.ip_frame.refresh()


def main():
    from src.engine.network_tools.ipv4.ipv4_addrress_configuration import IPV4AddressConfiguration
    root = tk.Tk()
    root.title('Windows IP Manager')
    ip_manager = IPManager(root, NetworkService(IPV4AddressConfiguration()))
    ip_manager.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
