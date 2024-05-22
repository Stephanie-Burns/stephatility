
import os
import re
import subprocess
import threading

from src.constants import MODIFY_HOSTS_BAT
from src.application_config.logger import app_logger


class LocalFileServer:
    def __init__(self, thread_manager: 'ThreadManager'):
        self.thread_manager = thread_manager
        self.server_process = None
        self.server_thread_id = None

    def start_server(self, directory: str, port: str):
        if not self.validate_directory(directory):
            raise ValueError("Invalid directory")
        if not self.validate_port(port):
            raise ValueError("Invalid port")

        self.server_thread_id = self.thread_manager.add_thread(target=self.run_server, args=(directory, port))
        app_logger.info(f"Hosting {directory} @ http://localhost:{port}...")

    def run_server(self, directory: str, port: int, stop_event: threading.Event):
        try:
            os.chdir(directory)
            self.server_process = subprocess.Popen(
                ["python", "-m", "http.server", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            app_logger.info(f"Hosting files from {directory} on port {port} with PID {self.server_process.pid}")

            while not stop_event.is_set():
                if self.server_process.poll() is not None:
                    break
                stop_event.wait(1)
        except Exception as e:
            app_logger.exception("Server crashed unexpectedly. %s", e)
        finally:
            self.terminate_server()

    def terminate_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            app_logger.info(f"Stopped Server with PID {self.server_process.pid}")
            self.server_process = None

    def stop_server(self):
        if self.server_thread_id:
            app_logger.info(f"Stopping server with PID {self.server_process.pid}...")
            self.thread_manager.stop_thread(self.server_thread_id)
            self.terminate_server()

    @staticmethod
    def validate_directory(directory: str) -> bool:
        if not directory:
            app_logger.error("No directory selected.")
            return False

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                app_logger.info(f"Directory created: {directory}")
            except OSError as e:
                app_logger.error(f"Failed to create directory: {e}")
                return False
        return True

    @staticmethod
    def validate_port(port: str) -> bool:
        return port.isdigit() and 1 <= int(port) <= 65535

    @staticmethod
    def validate_url(domain: str) -> bool:
        """Validate the local domain to ensure it contains only allowed characters."""
        pattern = r'^[a-zA-Z0-9._-]+$'
        return re.match(pattern, domain) is not None

    @staticmethod
    def modify_host_file(new_name, old_name=""):
        """
        Modifies the hosts file using a batch script and PowerShell for elevated privileges.

        Args:
            new_name (str): The new hostname to add.
            old_name (str): The old hostname to remove.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """

        old_name = new_name if not old_name else old_name
        batch_file_path = MODIFY_HOSTS_BAT
        args = f'"{new_name}" "{old_name}"'
        ps_command = f'Powershell -Command "Start-Process \'{batch_file_path}\' -ArgumentList \'{args}\' -Verb RunAs"'
        subprocess.check_output(ps_command, shell=True)

    @staticmethod
    def friendly_name_exists(friendly_name: str) -> bool:
        hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"

        with open(hosts_file_path, 'r') as hosts_file:
            for line in hosts_file:
                if friendly_name in line:
                    return True

        return False

    def set_friendly_name(self, new_friendly_name: str, current_friendly_name: str) -> None:
        try:
            if self.friendly_name_exists(new_friendly_name):
                return

            self.modify_host_file(new_friendly_name, current_friendly_name)

        except PermissionError as e:
            raise PermissionError("Permission Error", str(e))

        except OSError as e:
            raise OSError("File Error", str(e))

        except Exception as e:
            raise Exception("Error", str(e))
