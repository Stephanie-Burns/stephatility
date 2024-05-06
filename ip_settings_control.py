
import tkinter as tk
from octet_widget import OctetWidget


class IPSettingsControl(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("IP Configuration")
        self.geometry("350x210")
        self.resizable(False, False)

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
        tk.Label(adapter_frame, text="Ethernet Adapter: ").grid(row=0, column=0, sticky='w')
        adapter_entry = tk.Entry(adapter_frame, width=20)
        adapter_entry.insert(0, "Ethernet")
        adapter_entry.grid(row=0, column=2, sticky='e')

        # Data for labels and octets
        data = {
            "IP Address": ["192", "168", "0", "1"],
            "Subnet Mask": ["255", "255", "255", "0"],
            "Default Gateway": ["192", "168", "0", "254"]
        }

        # Create rows of labels and octet entries
        for i, (label_text, octets) in enumerate(data.items(), start=1):
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

            # Octet entries on the right
            octet_frame = tk.Frame(row_frame)
            octet_frame.grid(row=0, column=2, pady=5, sticky='e')

            for octet_position, octet_values in enumerate(octets):
                octet_widget = OctetWidget(octet_frame, octet_position, octet_values, update_callback=None)
                octet_widget.pack(side=tk.LEFT)

                if octet_position < 3:
                    dot_label = tk.Label(octet_frame, text=".")
                    dot_label.pack(side=tk.LEFT, padx=3)

        # Bottom frame for buttons
        button_frame = tk.Frame(container)
        button_frame.grid(row=5, column=0, sticky='ew', columnspan=3, pady=(10, 0))
        container.grid_columnconfigure(0, weight=1)

        # Buttons: Enter and Center
        cancel_button = tk.Button(button_frame, text="Enter", command=self.cancel_action)
        cancel_button.grid(row=0, column=0, sticky='ew', padx=(0, 10))

        enter_button = tk.Button(button_frame, text="Center", command=self.enter_action)
        enter_button.grid(row=0, column=1, sticky='ew', padx=(10, 0))

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
    app = IPSettingsControl()
    app.mainloop()
