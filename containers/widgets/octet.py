
import tkinter as tk
from typing import Callable, Optional

import enums


class Octet(tk.Entry):
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
        master (tk.Widget): The parent widget.
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
            master                      : tk.Widget,
            position                    : int,
            initial_value               : str = "",
            update_callback             : Optional[Callable[..., None]] = None
    ):
        # Widget Setup
        super().__init__(master, width=3, justify='center')
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

    def _emit_update(self, *args, **kwargs):
        if self.update_callback:
            self.update_callback(*args, **kwargs)

    def _validate_input(self, new_value: str, char: str, action: str) -> bool:
        """Ensure only valid Arabic numerals are allowed to populate the entry box in accordance with RFC 791."""
        if action == enums.EntryValidation.INSERT:
            if not char.isdigit():
                return False

            if len(new_value) > 3:
                return False

            if new_value == '0':
                return False

            if new_value.startswith('0') and len(new_value) > 1:
                return False

            if int(new_value) > 254:
                return False

            self.after_idle(self._emit_update)
            return True

        self.after_idle(self._emit_update)
        return True  # Always allow deletion

    def _octet_value_threshold_reached(self) -> bool:
        """Determine if the current octet's value meets the criteria for being considered complete.

        An octet is deemed complete under two conditions:

        1. It contains exactly three digits.
        2. It contains two digits, both forming a valid segment of an IP address (26-99),
           ensuring no further valid digit can be added without exceeding the maximum octet value of 254.

        Returns:
            bool: True if the octet meets the completion criteria, otherwise False.
        """
        return self.get() and (len(self.get()) == 3 or (len(self.get()) == 2 and int(self.get()) > 25))

    def _on_key_press(self, event: tk.Event) -> str:
        """Handle key press for special navigation and auto-advance."""
        shift_pressed = event.state == enums.SHIFT_MODIFIER_APPLIED_CODE
        first_octet = self.position == 0

        if event.keysym in (enums.KeySym.Return, enums.KeySym.KP_Enter):

            if shift_pressed:
                if not first_octet:
                    self._modify_focus(reverse=True)
                    return enums.EventAction.BREAK
                else:
                    return enums.EventAction.BREAK
            else:
                self._modify_focus()
                return enums.EventAction.BREAK

        elif event.keysym == enums.KeySym.Tab:
            self._modify_focus()
            return enums.EventAction.BREAK

        elif event.keysym == enums.KeySym.ISO_Left_Tab:
            self._modify_focus(reverse=True)
            return enums.EventAction.BREAK

        elif event.char == enums.KeySym.Period:
            self._modify_focus()
            return enums.EventAction.BREAK

    def _on_key_release(self, event: tk.Event) -> None:
        """Actions to preform when a key is released."""
        key_is_digit = event.keycode in enums.DIGIT_KEYCODES

        if key_is_digit and self._octet_value_threshold_reached():
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

    def _on_tab_press(self, event: tk.Event) -> str:
        """Advance focus to the next widget on tab press."""
        self._modify_focus()
        return enums.EventAction.BREAK

    def _on_shift_tab_press(self, event: tk.Event) -> str:
        """Advance focus to the previous widget on shift+tab press."""
        self._modify_focus(reverse=True)
        return enums.EventAction.BREAK


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
