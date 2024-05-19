
import os
import subprocess
import threading

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

    def validate_directory(self, directory: str) -> bool:
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

    def validate_port(self, port: str) -> bool:
        return port.isdigit() and 1 <= int(port) <= 65535
