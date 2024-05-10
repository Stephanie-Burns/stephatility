
import tkinter as tk

from typing import Callable, List, Optional
from containers.widgets.octet import Octet


class IPV4AddressBox(tk.Frame):
    def __init__(
            self,
            parent          : tk.Widget,
            current_ip      : List[str],
            update_callback : Optional[Callable[..., None]] = None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        # Public Attributes
        self.update_callback = update_callback

        # Private Attributes
        self._current_ip = current_ip

        # Frame - Directory Cleaner
        self.grid(sticky='ew', padx=10, pady=10)

        # Entry - Octet
        for i in range(4):
            initial_value = self._current_ip[i]
            octet = Octet(
                self,
                i,
                initial_value=initial_value,
                update_callback=self._on_octet_change
            )
            octet.grid(column=2 * i, row=0, padx=(0, 0))
            self.grid_columnconfigure(2 * i, weight=1)

            # Label - Octet Seperator: '.'
            if i < 3:
                dot_label = tk.Label(self, text=".")
                dot_label.grid(column=2 * i + 1, row=0, padx=3)
                self.grid_columnconfigure(2 * i + 1, weight=0)

    @property
    def ip_address(self) -> str:
        """Property to get the current IP address as a formatted string."""
        return '.'.join(self._current_ip)

    def _on_octet_change(self, position: int, new_value: str) -> None:

        if position is None or new_value is None:
            return

        if self._current_ip[position] != new_value:
            self._current_ip[position] = new_value
            self._emit_update()

    def _emit_update(self, *args, **kwargs):
        print(self.ip_address)
        print("IP Address Changed Update, P.S. dont forget to wire it up. :)")

        if self.update_callback:
            self.update_callback(*args, **kwargs)


def main():
    root = tk.Tk()
    root.geometry("300x100")

    current_ip = "192.38.22.56".split('.')
    ip_address_frame = IPV4AddressBox(root, current_ip)
    ip_address_frame.pack(fill='both', expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
