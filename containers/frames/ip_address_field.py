import tkinter as tk

from typing import List
from containers.widgets.octet import Octet


class IPV4AddressBox(tk.Frame):
    def __init__(self, parent, current_ip: List[str], **kwargs):
        super().__init__(parent, **kwargs)

        # Public Attributes
        self.current_ip = current_ip

        # Frame - Directory Cleaner
        self.parent = parent
        self.grid(sticky='ew', padx=10, pady=10)

        # Entry - Octet
        for i in range(4):
            initial_value = self.current_ip[i]
            octet = Octet(
                self,
                i,
                initial_value=initial_value,
                update_callback=self.on_octet_change
            )
            octet.grid(column=2 * i, row=0, padx=(0, 0))
            self.grid_columnconfigure(2 * i, weight=1)

            # Label - Octet Seperator: '.'
            if i < 3:
                dot_label = tk.Label(self, text=".")
                dot_label.grid(column=2 * i + 1, row=0, padx=3)
                self.grid_columnconfigure(2 * i + 1, weight=0)

    def on_octet_change(self):

        print("Octet changed, P.S. dont forget to wire it up. :)")


def main():
    root = tk.Tk()
    root.geometry("300x100")

    current_ip = "192.38.22.56".split('.')
    ip_address_frame = IPV4AddressBox(root, current_ip)
    ip_address_frame.pack(fill='both', expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
