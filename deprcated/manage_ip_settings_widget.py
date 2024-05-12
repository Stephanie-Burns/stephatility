import tkinter as tk
from tkinter import Toplevel, Entry, Frame, Button

from containers.widgets.octet import Octet

class IPManagementFrame(Toplevel):
    def __init__(self, parent, current_ip, update_callback=None):
        super().__init__(parent)
        self.title("IP Settings Management")
        # self.geometry("600x400")  # Adjust size as needed
        # self.resizable(False, False)

        self.current_ip = current_ip.split('.')
        self.update_callback = update_callback

        self.init_ui()

        # Make the window modal
        self.transient(parent)  # Set to be a transient window of its parent
        self.grab_set()  # Direct all events to this window
        self.wait_window(self)  # Wait here until this window is destroyed

    def init_ui(self):
        #cool label
        # Label(self, text="Manage IP Settings", font=('Arial', 16)).grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.grid_columnconfigure(0, weight=0)  # Column for the label
        self.grid_columnconfigure(1, weight=1)  # Middle column that takes up extra space
        self.grid_columnconfigure(2, weight=0)  # Column for the entry


        # Label(self, text="Ethernet Adapter: ", width=30).grid(row=0, column=0, padx=(0, 5), pady=10, sticky='w')
        # self.description_entry = Entry(self, width=20)
        # self.description_entry.grid(row=0, column=2, padx=(20, 25), pady=0, sticky='e')

        # Frame to hold the label and entry, ensuring they are managed together
        ethernet_adapter_frame = tk.Frame(self)
        ethernet_adapter_frame.grid(row=0, column=0, padx=(10, 10), pady=10, sticky='ew', columnspan=3)
        ethernet_adapter_frame.grid_columnconfigure(0, weight=1)
        ethernet_adapter_frame.grid_columnconfigure(1, weight=1)

        # Label on the left within the frame
        label = tk.Label(ethernet_adapter_frame, text="Ethernet Adapter: ")
        label.grid(row=0, column=0, padx=(0, 5), pady=10, sticky='w')

        # Entry on the right within the frame
        description_entry = tk.Entry(ethernet_adapter_frame, width=20)
        description_entry.grid(row=0, column=1, padx=(5, 0), pady=10, sticky='e')

        # Configure the main window to allow the top_frame to expand fully
        self.grid_columnconfigure(0, weight=1)

        # Frames for groups of octets
        self.ip_frame1 = Frame(self)
        self.ip_frame1.grid(row=1, column=0, padx=(10, 10), pady=10, sticky='ew', columnspan=3)
        self.ip_frame1.grid_columnconfigure(0, weight=1)
        self.ip_frame1.grid_columnconfigure(1, weight=1)


        self.ip_frame2 = Frame(self)
        self.ip_frame2.grid(row=2, column=0, padx=(10, 10), pady=10, sticky='ew', columnspan=3)
        self.ip_frame2.grid_columnconfigure(0, weight=1)
        self.ip_frame2.grid_columnconfigure(1, weight=1)

        self.ip_frame3 = Frame(self)
        self.ip_frame3.grid(row=3, column=0, padx=(10, 10), pady=10, sticky='ew', columnspan=3)
        self.ip_frame3.grid_columnconfigure(0, weight=1)
        self.ip_frame3.grid_columnconfigure(1, weight=1)

        self.create_octet_row(self.ip_frame1, "IP Address: ", self.current_ip)
        self.create_octet_row(self.ip_frame2, "Subnet Mask: ", ["55"] * 4)  # Example for empty octets
        self.create_octet_row(self.ip_frame3, "Default Gateway: ", [""] * 4)

        # Control buttons
        Button(self, text="Apply", width=10, command=self.apply_changes).grid(row=4, column=0, padx=10, pady=10, sticky='e')
        Button(self, text="Cancel", width=10,  command=self.destroy).grid(row=4, column=2, padx=10, pady=10, sticky='w')

    def create_octet_row(self, frame, label_text: str, ip):

        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        ip_frame = tk.Frame(frame)
        ip_frame.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        for i in range(4):
            octet = Octet(
                ip_frame,
                i,
                initial_value='192',
                # update_callback=self._update_set_button_state
            )

            octet.grid(row=0, column=2 * i, padx=(0, 5))  # Grid allows precise placement

            if i < 3:
                dot_label = tk.Label(ip_frame, text=".")
                dot_label.grid(row=0, column=2 * i + 1)  # Position dots between octets

    def apply_changes(self):
        # Logic to apply changes goes here
        if self.update_callback:
            new_ip = self.get_ip_entries()
            self.update_callback(new_ip)
        self.destroy()

    def get_ip_entries(self):
        # Retrieve the IP address from entries (this will be simplified for demonstration)
        return ".".join(entry.get() for entry in self.ip_frame1.winfo_children() if isinstance(entry, Entry))

    def destroy(self):
        print("Closing IP management window")
        if self.update_callback:
            self.update_callback()
        super().destroy()



def main():

    def open_ip_manager(toplevel_frame):
        # This will create a new Toplevel window each time it's clicked
        IPManagementFrame(toplevel_frame, "192.168.1.100", update_callback=None)


    root = tk.Tk()
    root.title("Octet Widget Demo")
    root.geometry("300x100")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    tk.Button(frame, text="Manage", command=lambda: open_ip_manager(root)).pack(side=tk.BOTTOM)

    root.mainloop()


if __name__ == "__main__":
    main()
