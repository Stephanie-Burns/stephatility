
import tkinter as tk


class BlueLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg='#010101', bg="#7393B3", font=("Arial", 14), **kwargs)
