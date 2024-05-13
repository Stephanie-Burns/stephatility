
import tkinter as tk

from gui import DirectoryCleaner, IPManager, TempFileGenerator
from network_tools import IPV4Address, IPV4AddressConfiguration, NetworkService


class UtilApp(tk.Frame):
    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)

        self.current_ip = IPV4Address.from_string("0.0.0.0")  # get from config or service
        self.network_service = NetworkService(IPV4AddressConfiguration())

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Initialize Containers
        self.directory_cleaner_0 = DirectoryCleaner(self,"C:/Viper")
        self.directory_cleaner_0.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        self.directory_cleaner_1 = DirectoryCleaner(self,"C:/ViperConfigData")
        self.directory_cleaner_1.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        self.tempfile_gen = TempFileGenerator(self)
        self.tempfile_gen.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        self.ip_manager = IPManager(self, self.current_ip, self.network_service)
        self.ip_manager.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)


def main():
    root = tk.Tk()
    root.title('StephAtility (lol)')
    app = UtilApp(root)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
