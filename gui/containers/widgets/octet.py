
import tkinter as tk
from typing import Callable, Optional

from gui import enums
from gui.mixins import CallbackMixin


class Octet(CallbackMixin, tk.Entry):
    """A widget representing a single octet (byte) of an IP address.

    An octet is an 8-bit field, which holds values from 1 to 254 in this context, as required for a valid IPv4 address.
    This widget ensures that the user can only input valid numeric values within the permissible range.

    Features:
    - Validates input according to IPv4 addressing standards for an octet. (RFC 791)
    - Navigates automatically to the next field once input is complete.
    - Allows navigation between fields using navigation keys.
    - Restores previous valid content if no changes are made.

    Note:
    - The input field is automatically cleared upon gaining focus to facilitate easy entry.
    - If focus is lost without entering a valid value, the previous valid value is restored.

    Args:
        parent (tk.Widget): The parent widget.
        position (int): The position of this octet within its group.
        initial_value (str, optional): The default value to be placed in the widget.
        update_callback (Callable[[], None], optional): A function to run when the widget updates.

    Key Bindings:
        - Enter/Return: Advances focus to the next octet.
        - Shift + Enter/Return moves focus to the previous octet if available.
        - Tab: Advances focus to the next octet.
        - Shift + Tab: Advances focus to the previous octet.
        - Period (dot): Advances focus to the next octet.
    """
    def __init__(
            self,
            parent                      : tk.Widget,
            position                    : int,
            initial_value               : str = "",
            update_callback             : Optional[Callable[..., None]] = None,
            **kwargs
    ):
        # Widget Setup
        super().__init__(update_callback, parent, width=3, justify='center', **kwargs)
        self.insert(0, initial_value)

        #  Public Attributes
        self.focus_travel_direction     = 0
        self.position                   = position
        self.previous_valid_content     = initial_value if initial_value else "-1"
        self.update_callback            = update_callback

        # Internal configuration for key input validation
        self.config(
            validate="key",
            validatecommand=(self.register(self._validate_input), '%P', '%S', '%d')
        )

        # Event Bindings
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)

        self.bind("<Shift-Return>", self._on_shift_key_press)
        self.bind("<Shift-KP_Enter>", self._on_shift_key_press)
        self.bind("<Shift-Tab>", self._on_shift_key_press)
        # self.bind("<ISO_Left_Tab>", self._on_shift_key_press) # Upsetting windows

    @staticmethod
    def _validate_input(new_value: str, char: str, action: str) -> bool:
        """Ensure only valid Arabic numerals are allowed to populate the entry box in accordance with RFC 791."""
        if action == enums.EntryValidation.INSERT:
            if not char.isdigit():
                return False

            if len(new_value) > 3:
                return False

            if new_value.startswith('0') and len(new_value) > 1:
                return False

            if int(new_value) > 255:
                return False

            return True

        return True  # Always allow deletion

    def _octet_value_threshold_reached(self) -> bool:
        """Determine if the current octet's value meets the criteria for being considered complete.

        An octet is deemed complete under the following conditions:

        1. It contains exactly three digits and equals "255".
        2. It contains exactly one digit and equals "0".
        3. It contains two digits and is between 26 and 99, ensuring no further valid digit can be added
           without exceeding the maximum octet value of 254.

        Returns:
            bool: True if the octet meets the completion criteria, otherwise False.
        """
        display_value = self.get()
        if display_value:

            if display_value == "255" or display_value == "0":
                return True
            elif len(display_value) == 2 and 26 <= int(display_value) <= 99:
                return True
            elif len(display_value) == 3 and 100 <= int(display_value) < 255:
                return True

        return False

    def _on_key_press(self, event: tk.Event) -> str:
        """Handle key press for special navigation and auto-advance without Shift key."""
        if event.keysym in (
                enums.KeySym.RETURN,
                enums.KeySym.KP_Enter,
                enums.KeySym.TAB
        ) or event.char == enums.KeySym.PERIOD:
            self._modify_focus()
            return enums.EventAction.BREAK

    def _on_shift_key_press(self, event: tk.Event) -> str:
        """Handle shift-modified key presses for navigation."""
        first_octet = self.position == 0

        if event.keysym in (enums.KeySym.RETURN, enums.KeySym.KP_Enter, enums.KeySym.TAB):
            if not first_octet:
                self._modify_focus(reverse=True)
            return enums.EventAction.BREAK

        elif event.keysym == enums.KeySym.ISO_Left_Tab:
            self._modify_focus(reverse=True)
            return enums.EventAction.BREAK

    def _on_key_release(self, event: tk.Event) -> None:
        """Actions to preform when a key is released."""
        display_value = self.get()

        if display_value and display_value != self.previous_valid_content:
            self.emit_update(self.position, display_value)

        if self._octet_value_threshold_reached():
            self.after_idle(self._modify_focus)

    def _on_focus_in(self, event: tk.Event) -> None:
        """Clear entry temporarily when gaining focus if it's not empty."""
        current_value = self.get()
        if current_value:
            self.previous_valid_content = current_value
            self.delete(0, tk.END)

    def _on_focus_out(self, event: tk.Event) -> None:
        """Restore previous content if no valid entry is made."""
        if not self.get():
            self.insert(0, self.previous_valid_content)

    def _modify_focus(self, reverse: bool = False) -> None:
        """Change focus to the next or previous widget based on the direction."""
        self.focus_travel_direction = -1 if reverse else 1
        next_widget = self.tk_focusPrev() if reverse else self.tk_focusNext()
        next_widget.focus_set()


def main():
    root = tk.Tk()
    root.title("Octet Widget Demo")
    root.geometry("300x100")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Initialize two octets for demonstration
    octet1 = Octet(frame, position=0, initial_value="192")
    octet2 = Octet(frame, position=1, initial_value="168")

    octet1.pack(side=tk.LEFT, padx=5)
    octet2.pack(side=tk.LEFT, padx=5)

    tk.Button(frame, text="Quit", command=root.quit).pack(side=tk.BOTTOM)

    root.mainloop()


if __name__ == "__main__":
    main()
