import tkinter as tk


class DraggableListbox(tk.Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind('<Button-1>', self._select)
        self.bind('<B1-Motion>', self._move)
        self.curIndex = None

    def _select(self, event):
        # This method will capture the index of the item selected
        self.curIndex = self.nearest(event.y)

    def _move(self, event):
        # This method will handle the dragging and rearranging of the items
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Entry widget to add new items
        self.entry = tk.Entry(self)
        self.entry.pack(side="top", fill="x")

        # Button to add items from the entry to the listbox
        self.add_button = tk.Button(self, text="Add", command=self.add_item)
        self.add_button.pack(side="top")

        # Listbox initialized from the custom draggable class
        self.listbox = DraggableListbox(self)
        self.listbox.pack(side="top", fill="both", expand=True)

        # Button to remove selected items from the listbox
        self.remove_button = tk.Button(self, text="Remove", command=self.remove_item)
        self.remove_button.pack(side="top")

    def add_item(self):
        # Add items to the listbox and clear the entry field
        item = self.entry.get()
        if item:
            self.listbox.insert("end", item)
            self.entry.delete(0, "end")

    def remove_item(self):
        # Remove selected items from the listbox
        try:
            index = self.listbox.curselection()
            self.listbox.delete(index)
        except:
            pass  # Handle the case where no item is selected

root = tk.Tk()
app = Application(master=root)
app.mainloop()
