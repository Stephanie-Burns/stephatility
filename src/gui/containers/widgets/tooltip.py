
import tkinter as tk


class ToolTip:
    """
    A class to create and manage tooltips for tkinter widgets.

    Attributes:
        widget (tk.Widget): The widget to which the tooltip is attached.
        text (str): The text to be displayed in the tooltip.
        offset_x (int): The x-offset of the tooltip from the widget.
        offset_y (int): The y-offset of the tooltip from the widget.
    """
    def __init__(self, widget, text, offset_x=25, offset_y=25):
        self.widget = widget
        self.text = text
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tip_window = None
        self.widget.bind("<Enter>", self._show_tooltip)
        self.widget.bind("<Leave>", self._hide_tooltip)

    def _show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + self.offset_x
        y = y + self.widget.winfo_rooty() + self.offset_y
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))

        # Label - ToolTip Display
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def _hide_tooltip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def add_tooltip(widget, text, offset_x=25, offset_y=25):
    """
    Attach a tooltip to a widget.

    Args:
        widget (tk.Widget): The widget to which the tooltip is attached.
        text (str): The text to be displayed in the tooltip.
        offset_x (int): The x-offset of the tooltip from the widget.
        offset_y (int): The y-offset of the tooltip from the widget.

    Returns:
        tk.Widget: The widget with the attached tooltip.
    """
    ToolTip(widget, text, offset_x, offset_y)
    return widget


class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tooltip Demo")

        button = add_tooltip(tk.Button(self, text="Hover over me!"), "This is a button", offset_x=30, offset_y=30)
        button.pack(pady=20, padx=20)

        entry = add_tooltip(tk.Entry(self), "This is an entry widget", offset_x=-50, offset_y=50)
        entry.pack(pady=20, padx=20)


if __name__ == "__main__":
    app = DemoApp()
    app.mainloop()
