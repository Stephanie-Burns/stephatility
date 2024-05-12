## Octet Widget for IPv4 Addresses

### Overview
The `OctetWidget` is a specialized tkinter entry widget designed for input of individual octets in IPv4 addresses. It ensures that only numerically valid IP address components are entered, adhering to both usability and RFC 791 standards.

### Features
- **Strict Validation:** Only allows numbers between 1 and 254, preventing illegal IP address entries.
- **Auto-navigation:** Moves focus to the next or previous widget upon completion of a valid entry or via navigation keys.
- **State Restoration:** Automatically restores the previous valid entry if focus is lost without a new valid number.

### Usage
The widget is intended for use in environments where IPv4 address input is required, ensuring that each octet entered is within the valid range specified by Internet Protocol standards.

```python
octet = OctetWidget(master, position=1, initial_value='100')
```

### Key Bindings
- Enter/Return and KP_Enter: Moves focus to the next widget.
- Shift + Enter/Return: Moves focus to the previous widget, unless it is the first one.
- Tab: Advances focus to the next widget.
- Shift + Tab: Moves focus to the previous widget.
- Period ('.'): Similar to Enter, advances focus to the next widget.
- Implementation Details
- The widget uses tkinter's validation mechanism to filter keystrokes, allowing only numerically valid input. It uses the following parameters for its setup:

### Implementation Details
The widget uses tkinter's validation mechanism to filter keystrokes, allowing only numerically valid input. It uses the following parameters for its setup:

- master: Parent tkinter widget.
- position: Numeric position in the sequence of octet widgets.
- initial_value: Initial value to display in the widget.
- update_callback: A callback function triggered on updates.

# Example
Here is a basic example of how to set up and use the OctetWidget within a tkinter application:

```python
import tkinter as tk
from gui.containers.widgets import OctetWidget


def main():
    root = tk.Tk()
    root.geometry('200x50')

    octet1 = OctetWidget(root, position=0, initial_value='192', update_callback=my_update_function)
    octet1.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
```
Replace my_update_function with the function you want to trigger when the widget is updated. This setup will create a window with a single octet entry box initialized to '192'.
