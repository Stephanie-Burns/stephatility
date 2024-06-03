
import tkinter as tk
from tkinter import ttk


class ScrollableTextArea(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - Self
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Text Area
        self.text_area = tk.Text(self, wrap='word')
        self.text_area.grid(row=0, column=0, sticky='nsew')

        # Scrollbar - Vertical
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.text_area.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Bindings
        self.text_area['yscrollcommand'] = self.scrollbar.set

    def get_text(self) -> str:
        """Return the current content of the text area."""
        return self.text_area.get('1.0', tk.END).strip()

    def set_text(self, text: str):
        """Set the content of the text area."""
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', text)


# Example usage
class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Scrollable Text Area Example')
        self.geometry('400x300')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_text_area = ScrollableTextArea(self)
        self.scrollable_text_area.grid(row=0, column=0, sticky='nsew')

        # Set some initial text
        self.scrollable_text_area.set_text('This is some initial text.')

        # Print the current text after 2 seconds
        self.after(2000, self.print_text)

    def print_text(self):
        print(self.scrollable_text_area.get_text())


if __name__ == '__main__':
    app = DemoApp()
    app.mainloop()
