
import tkinter as tk

from src.gui.containers.frames.ip_address_field import IPV4AddressBox
from src.gui.mixins import CallbackMixin
from src.network_tools import IPV4Address, NetworkService


class IPSettingsModal(CallbackMixin, tk.Toplevel):
    def __init__(self, parent, network_service: NetworkService, update_callback=None, **kwargs):
        super().__init__(update_callback, parent, **kwargs)
        self.title("IP Configuration")
        self.geometry("350x260")
        self.resizable(False, False)

        self.network_service = network_service
        self.selected_network = None

        self.network_configuration = {
            "IP Address": IPV4Address.from_string('192.168.0.100'),
            "Subnet Mask": IPV4Address.from_string('255.255.255.0'),
            "Default Gateway": IPV4Address.from_string('192.168.0.1'),
        }

        # Main container frame
        container = tk.Frame(self)
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        # Manually create the Ethernet Adapter row
        adapter_frame = tk.Frame(container)
        adapter_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        adapter_frame.grid_columnconfigure(0, weight=1)
        adapter_frame.grid_columnconfigure(1, weight=2)  # Central expanding spacer
        adapter_frame.grid_columnconfigure(2, weight=1)

        # Label and Entry for Ethernet Adapter
        tk.Label(adapter_frame, text="Adapter Name: ").grid(row=0, column=0, sticky='w')
        adapter_entry = tk.Entry(adapter_frame, width=20)
        adapter_entry.insert(0, "Ethernet")
        adapter_entry.grid(row=0, column=2, sticky='e')

        # Data for labels and octets
        labels = ("IP Address", "Subnet Mask", "Default Gateway")
        addrs = (
            self.network_service.network_config.ipv4_address,
            self.network_service.network_config.subnet_mask,
            self.network_service.network_config.default_gateway
        )

        # ==========
        # Frame to hold the radio buttons
        radio_frame = tk.Frame(adapter_frame)
        radio_frame.grid(row=1, column=2, sticky="ew", pady=(5, 10))

        tk.Label(adapter_frame, text="Adapter Type: ").grid(row=1, column=0, sticky='w')

        # Configure the frame's column weights to ensure it expands fully
        radio_frame.grid_columnconfigure(0, weight=1)
        radio_frame.grid_columnconfigure(1, weight=1)

        # Variable to hold the selected value
        self.selected_network = tk.StringVar(value="Ethernet")  # Default to 'Ethernet'

        # Create radio buttons for network type selection
        ethernet_radio = tk.Radiobutton(radio_frame, text="Ethernet", variable=self.selected_network, value="Ethernet")
        wifi_radio = tk.Radiobutton(radio_frame, text="WiFi", variable=self.selected_network, value="WiFi")

        # Position the radio buttons side by side within the frame
        ethernet_radio.grid(row=0, column=0, sticky="ew")
        wifi_radio.grid(row=0, column=1, sticky="ew")

        # ============

        # Create labels and ip fields
        data = {
            "IP Address"        : self.network_service.network_config.ipv4_address,
            "Subnet Mask"       : self.network_service.network_config.subnet_mask,
            "Default Gateway"   : self.network_service.network_config.default_gateway
        }

        for i, (label_text, ip_address) in enumerate(data.items(), start=2):
            row_frame = tk.Frame(container)
            row_frame.grid(row=i, column=0, sticky='ew')
            container.grid_columnconfigure(0, weight=1)

            # Configure columns for label, spacer, and octets
            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=2)  # Central expanding spacer
            row_frame.grid_columnconfigure(2, weight=1)

            # Label on the left
            label = tk.Label(row_frame, text=label_text)
            label.grid(row=0, column=0, sticky='w')

            address_box = IPV4AddressBox(row_frame, ip_address, update_callback=self._check_apply_button_state)
            address_box.grid(row=0, column=2, padx=(10, 0), pady=5, sticky='e')

        # Bottom frame for buttons
        button_frame = tk.Frame(container)
        button_frame.grid(row=5, column=0, sticky='ew', columnspan=3, pady=(10, 0))
        container.grid_columnconfigure(0, weight=1)

        # Buttons: Enter and Center
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_action)
        cancel_button.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(10, 10))

        self.apply_button = tk.Button(button_frame, text="Apply", command=self.apply_action)
        self.apply_button.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(10, 10))

        # Ensure buttons fill their space
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self._check_apply_button_state()

    def apply_action(self):
        print("IP settings Modal: Apply button clicked")

        self.network_service.apply_configuration()
        self.network_service.network_config.reset_baseline()
        self.emit_update()
        self._check_apply_button_state()
        self.destroy()

    def _check_apply_button_state(self) -> None:
        if self.network_service.network_config.has_changed():
            self.apply_button.config(state='normal')
        else:
            self.apply_button.config(state='disabled')

    def cancel_action(self):
        print("IP settings Modal: Cancel button clicked")
        print(self.network_service.network_config)
        self.destroy()


if __name__ == "__main__":
    def open_modal():
        from src.network_tools.ipv4_addrress_configuration import IPV4AddressConfiguration
        modal = IPSettingsModal(root, NetworkService(IPV4AddressConfiguration))
        modal.transient(root)
        modal.grab_set()

    root = tk.Tk()
    root.title("Main Application Window")
    root.geometry("600x400")

    # Button to open the modal
    open_button = tk.Button(root, text="Open IP Settings", command=open_modal)
    open_button.pack(pady=20)

    root.mainloop()
