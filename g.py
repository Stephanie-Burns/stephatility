import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class NetworkManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Manager")

        # Network Settings Frame
        self.network_frame = ttk.LabelFrame(self, text="Network Configuration")
        self.network_frame.grid(padx=10, pady=10, sticky="ew")

        # Entry Widgets for Network Configuration
        self.adapter_name_var = tk.StringVar()
        self.gateway_var = tk.StringVar()
        self.subnet_var = tk.StringVar()

        ttk.Label(self.network_frame, text="Adapter Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.network_frame, textvariable=self.adapter_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.network_frame, text="Gateway:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.network_frame, textvariable=self.gateway_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.network_frame, text="Subnet:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.network_frame, textvariable=self.subnet_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.network_frame, text="Save", command=self.save_network_config).grid(row=3, column=1, padx=5, pady=5)

        # IP Change Section
        self.ip_change_frame = ttk.LabelFrame(self, text="Change IP")
        self.ip_change_frame.grid(padx=10, pady=10, sticky="ew")

        self.new_ip_var = tk.StringVar()
        ttk.Label(self.ip_change_frame, text="Change IP:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.ip_change_frame, textvariable=self.new_ip_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.ip_change_frame, text="Manage", command=self.manage_ip).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.ip_change_frame, text="Run", command=self.run_ip_change).grid(row=1, column=1, padx=5, pady=5)

    def save_network_config(self):
        # Logic to save network configuration
        pass

    def manage_ip(self):
        # Logic to manage IP settings
        pass

    def run_ip_change(self):
        # Call to script to change IP
        new_ip = self.new_ip_var.get()
        result = subprocess.run(['python', 'change_ip_script.py', new_ip], capture_output=True, text=True)
        messagebox.showinfo("Result", result.stdout)

if __name__ == "__main__":
    app = NetworkManagerApp()
    app.mainloop()
