
import tkinter as tk
import tkinter.ttk as ttk

from src.application_config.app_logger import app_logger
from src.gui.containers.frames import IPV4AddressBox
from src.gui.containers.toplevel import IPSettingsModal
from src.engine.network_center import NetworkService
from src.gui.containers.widgets.blue_label import BlueLabel
from src.gui.containers.widgets.blue_button import BlueButton
from src.constants import Colors


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
        self.config(bg=Colors.BLUE_GRAY)
        self.grid(sticky=tk.EW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Label - IP Address
        self.label = BlueLabel(self, text="IP Address:")
        self.label.grid(row=0, column=0, padx=(10, 0), pady=0, sticky=tk.W)

        #  Frame - IPV4 Address Box
        self.ip_frame = IPV4AddressBox(
            self,
            self.network_service.network_config.ipv4_address,
            self._check_apply_button_state,
        )
        self.ip_frame.grid(row=0, column=1, padx=(0, 16), pady=0, sticky=tk.EW)

        # Button - Apply
        self.apply_button = ttk.Button(
            self,
            text="Apply",
            style="Blue.TButton",
            command=self._set_ip_address,
        )
        self.apply_button.grid(row=0, column=2, padx=(0, 65), pady=0, sticky=tk.EW)
        self.apply_button.bind('<Return>', self._on_enter)
        self.apply_button.bind('<KP_Enter>', self._on_enter)

        # Button - Manage
        self.manage_button = ttk.Button(
            self,
            text="Manage",
            style="Blue.TButton",
            command=self._launch_manage_ip_modal
        )
        self.manage_button.grid(row=0, column=3, padx=(0, 0), pady=0, sticky=tk.EW)

        self._check_apply_button_state()       # Initial check

    def _check_apply_button_state(self) -> None:
        if self.network_service.network_config.has_changed():
            self.apply_button.state(["!disabled"])
        else:
            self.apply_button.state(["disabled"])

    def _set_ip_address(self):
        app_logger.info(
            "Changing IP from %s, to: %s",
            self.network_service.network_config.previous_config.get('ipv4_address'),
            self.network_service.network_config.ipv4_address
        )

        self.network_service.apply_configuration()
        self.network_service.network_config.reset_baseline()
        self._check_apply_button_state()

        # Remove focus from entry widgets
        self.focus_set()

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
    from src.engine.network_center.ipv4.ipv4_addrress_configuration import IPV4AddressConfiguration
    root = tk.Tk()
    root.title('Windows IP Manager')
    ip_manager = IPManager(root, NetworkService(IPV4AddressConfiguration()))
    ip_manager.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
