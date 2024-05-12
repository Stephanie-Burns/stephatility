
from typing import Callable, Optional, Any


class CallbackMixin:
    def __init__(self, update_callback: Optional[Callable[..., None]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_callback = update_callback

    def emit_update(self, *args: Any, **kwargs: Any) -> None:
        """Invoke the update callback with provided arguments, if it exists."""
        if self.update_callback:
            try:
                self.update_callback(*args, **kwargs)
            except Exception as e:
                print(f"Error during callback execution: {e}")
