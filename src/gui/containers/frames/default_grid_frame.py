
import tkinter as tk


class DefaultGridFrame(tk.Frame):
    """4x4 grid frame"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_grid()

    def setup_grid(self):
        """Set up the grid configuration with uniform column weights and padding."""
        self.grid(sticky='ew', padx=10, pady=10)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
