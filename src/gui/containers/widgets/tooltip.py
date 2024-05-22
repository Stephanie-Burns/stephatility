import tkinter as tk
from tkinter import LEFT

class ToolTip:
    def __init__(self, widget, text, position='n', offset_x=10, offset_y=10):
        self.widget = widget
        self.text = text
        self.position = position
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tip_window = None

        self.widget.bind("<Enter>", self._show_tooltip)
        self.widget.bind("<Leave>", self._hide_tooltip)

    def _calculate_position(self):
        widget_x = self.widget.winfo_rootx()
        widget_y = self.widget.winfo_rooty()
        widget_width = self.widget.winfo_width()
        widget_height = self.widget.winfo_height()
        x, y = 0, 0

        if self.position == 'n':
            x = widget_x + widget_width // 2
            y = widget_y - self.offset_y
        elif self.position == 's':
            x = widget_x + widget_width // 2
            y = widget_y + widget_height + self.offset_y
        elif self.position == 'e':
            x = widget_x + widget_width + self.offset_x
            y = widget_y + widget_height // 2
        elif self.position == 'w':
            x = widget_x - self.offset_x
            y = widget_y + widget_height // 2

        # Apply the offsets
        if self.position in ['n', 's']:
            x += self.offset_x
        else:
            y += self.offset_y

        return x, y

    def _show_tooltip(self, event=None):
        if self.tip_window or not self.text:
            return

        x, y = self._calculate_position()

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify=LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def _hide_tooltip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

def add_tooltip(widget, text, position='n', offset_x=10, offset_y=10):
    ToolTip(widget, text, position, offset_x, offset_y)

class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tooltip Demo")

        # Button with north tooltip
        button_n = tk.Button(self, text="Hover over me (N)!")
        button_n.pack(pady=(100, 30), padx=20)
        add_tooltip(button_n, "This is a north tooltip\nwith multiple lines.", position='n', offset_x=0, offset_y=10)

        # Button with south tooltip
        button_s = tk.Button(self, text="Hover over me (S)!")
        button_s.pack(pady=10, padx=20)
        add_tooltip(button_s, "This is a south tooltip\nwith wrapping text and more content to show the wrap functionality.", position='s', offset_x=0, offset_y=10)

        # Button with east tooltip
        button_e = tk.Button(self, text="Hover over me (E)!")
        button_e.pack(pady=10, padx=20)
        add_tooltip(button_e, "This is an east tooltip", position='e', offset_x=10, offset_y=0)

        # Button with west tooltip
        button_w = tk.Button(self, text="Hover over me (W)!")
        button_w.pack(pady=10, padx=300)
        add_tooltip(button_w, "This is a west tooltip", position='w', offset_x=10, offset_y=0)

        # Entry widget with tooltip
        entry = tk.Entry(self)
        entry.pack(pady=10, padx=20)
        add_tooltip(entry, "This is an entry widget with a tooltip", position='e', offset_x=10, offset_y=0)

        # Canvas widget with tooltip (e.g., for ToggleButton)
        canvas = tk.Canvas(self, width=100, height=50, bg='lightgrey')
        canvas.pack(pady=10, padx=20)
        add_tooltip(canvas, "This is a canvas widget\nwith a tooltip.", position='n', offset_x=0, offset_y=10)

        # Label with tooltip
        label = tk.Label(self, text="Hover over this label!")
        label.pack(pady=10, padx=20)
        add_tooltip(label, "This is a label with a tooltip.", position='s', offset_x=0, offset_y=10)

if __name__ == "__main__":
    app = DemoApp()
    app.mainloop()
