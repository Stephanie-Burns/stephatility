
import threading
from typing import Callable


class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.locks = {}
        self.stop_events = {}
        self.lock = threading.Lock()

    def add_thread(self, target: Callable, args: tuple, daemon: bool = True) -> int:
        stop_event = threading.Event()
        thread = threading.Thread(target=target, args=args + (stop_event,))
        thread.daemon = daemon
        with self.lock:
            thread.start()
            self.threads[thread.ident] = thread
            self.locks[thread.ident] = threading.Lock()
            self.stop_events[thread.ident] = stop_event
            return thread.ident

    def stop_thread(self, identifier: int):
        with self.lock:
            stop_event = self.stop_events.pop(identifier, None)
            thread = self.threads.pop(identifier, None)
            if stop_event and thread:
                stop_event.set()
                thread.join()
                self.locks.pop(identifier, None)

    def stop_all_threads(self):
        with self.lock:
            for identifier, thread in list(self.threads.items()):
                stop_event = self.stop_events.pop(identifier, None)
                if stop_event:
                    stop_event.set()
                if thread.is_alive():
                    thread.join()
            self.threads.clear()
            self.locks.clear()
            self.stop_events.clear()
