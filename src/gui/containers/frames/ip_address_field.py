
import tkinter as tk

from typing import Callable, Optional

from src.gui.containers.widgets.octet import Octet
from src.gui.mixins import CallbackMixin
from src.network_tools import IPV4Address


class IPV4AddressBox(CallbackMixin, tk.Frame):
    def __init__(
            self,
            parent          : tk.Widget,
            ip_address      : IPV4Address,
            update_callback : Optional[Callable[..., None]] = None,
            **kwargs
    ):
        super().__init__(update_callback, parent, **kwargs)

        # Public Attributes
        self.ip_address = ip_address
        self.octets = []

        # Frame - IPV4Address Box
        self.grid(sticky='ew', padx=10, pady=10)

        # Entry - Octet
        for i in range(4):
            initial_value = self.ip_address[i]
            octet = Octet(
                self,
                i,
                initial_value=initial_value,
                update_callback=self._on_octet_change
            )
            octet.grid(column=2 * i, row=0, padx=(0, 0))
            self.grid_columnconfigure(2 * i, weight=1)
            self.octets.append(octet)

            # Label - Octet Seperator: '.'
            if i < 3:
                dot_label = tk.Label(self, text=".")
                dot_label.grid(column=2 * i + 1, row=0, padx=3)
                self.grid_columnconfigure(2 * i + 1, weight=0)

    def _on_octet_change(self, position: int, new_value: str) -> None:

        if position is None or new_value is None:
            return

        if self.ip_address[position] != new_value:
            self.ip_address[position] = new_value
            self.emit_update()

    def refresh(self):
        """Refresh the content of the IP address box."""
        for i in range(4):
            self.octets[i].delete(0, tk.END)
            self.octets[i].insert(0, self.ip_address[i])
            self.octets[i].previous_valid_content = self.ip_address[i]


def main():
    root = tk.Tk()
    root.geometry("300x100")

    current_ip = IPV4Address.from_string("192.38.22.56")
    ip_address_frame = IPV4AddressBox(root, current_ip)
    ip_address_frame.pack(fill='both', expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
