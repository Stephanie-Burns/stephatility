
import os
import tkinter as tk

from src.engine.network_center.network_center_settings import NetworkCenterSettings
from src.engine.network_center.http_server import ThreadManager
from src.engine.network_center.http_server.local_file_server import LocalFileServer
from src.engine.network_center import NetworkService
from src.engine.network_center.ipv4 import IPV4AddressConfiguration
from src.gui.containers.frames.directory_picker import DirectoryPickerRow
from src.gui.containers.frames.file_server import FileServerRow
from src.gui.containers.frames.localhost_setter import HRAddressRow
from src.gui.containers.ip_manager import IPManager


class NetworkCenter(tk.Frame):
    def __init__(self, parent: tk.Widget, user_settings: NetworkCenterSettings, thread_manager: ThreadManager, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.config(borderwidth=2, relief="sunken")

        self.directory_var = tk.StringVar(value=os.path.join(os.path.expanduser('~'), 'file-pile'))

        self.user_settings = user_settings
        self.thread_manager = thread_manager

        self.network_service = NetworkService(IPV4AddressConfiguration(), self.user_settings)
        self.network_service.get_network_configuration()

        self.file_server = LocalFileServer(self.thread_manager)

        self.ip_manager = IPManager(self, self.network_service)
        self.ip_manager.grid(row=0, column=0, sticky='ew')

        self.file_server_row = FileServerRow(self, self.file_server, self.directory_var)
        self.file_server_row.grid(row=1, column=0, sticky='ew')

        self.directory_picker_row = DirectoryPickerRow(self, self.directory_var)
        self.directory_picker_row.grid(row=2, column=0, sticky='ew')

        # self.hr_address_row = HRAddressRow(self, self.file_server, self.app_config.settings.http_file_server)
        # self.hr_address_row.grid(row=3, column=0, sticky='ew')

    def on_close(self):
        """Handle any cleanup necessary when the NetworkCenter is closed."""
        self.file_server.stop_server()
