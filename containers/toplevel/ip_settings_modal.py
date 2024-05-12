
import tkinter as tk

from containers.frames.ip_address_field import IPV4AddressBox


class IPSettingsModal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("IP Configuration")
        self.geometry("350x260")
        self.resizable(False, False)

        self.selected_network = None

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
        data = {
            "IP Address": ["192", "168", "0", "1"],
            "Subnet Mask": ["255", "255", "255", "0"],
            "Default Gateway": ["192", "168", "0", "254"]
        }

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

        # ==========

        # Create rows of labels and octet entries
        for i, (label_text, octets) in enumerate(data.items(), start=2):
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

            address_box = IPV4AddressBox(row_frame, octets)
            address_box.grid(row=0, column=2, padx=(10, 0), pady=5, sticky='e')

        # Bottom frame for buttons
        button_frame = tk.Frame(container)
        button_frame.grid(row=5, column=0, sticky='ew', columnspan=3, pady=(10, 0))
        container.grid_columnconfigure(0, weight=1)

        # Buttons: Enter and Center
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_action)
        cancel_button.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(10, 10))

        enter_button = tk.Button(button_frame, text="Apply", command=self.enter_action)
        enter_button.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(10, 10))

        # Ensure buttons fill their space
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def enter_action(self):
        # Placeholder for whatever action the Enter button should do
        print("Enter button clicked")
        self.destroy()

    def cancel_action(self):
        # Placeholder for whatever action the Center button should do
        print("Center button clicked")
        self.destroy()


if __name__ == "__main__":
    app = IPSettingsModal()
    app.mainloop()
