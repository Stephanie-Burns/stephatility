import tkinter as tk

import tkinter as tk


class BlueButton(tk.Button):
    def __init__(self, parent, **kwargs):
        # Set default values
        kwargs.setdefault('bg', '#778da4')
        kwargs.setdefault('disabledbackground', '#f0f0f0')
        kwargs.setdefault('width', 20)
        kwargs.setdefault('highlightbackground', "black")
        kwargs.setdefault('disabledforeground', "#7b7b7b")

        self.normal_bg = kwargs['bg']
        self.disabled_bg = kwargs.pop('disabledbackground')

        super().__init__(parent, **kwargs)

    def config(self, **kwargs):
        if 'state' in kwargs:
            state = kwargs['state']
            if state == 'disabled':
                self['bg'] = self.disabled_bg
            else:
                self['bg'] = self.normal_bg
        super().config(**kwargs)


class _BlueButtonDemo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(pady=20)

        self.default_disabled_bg_button = BlueButton(self, text="Default Disabled BG", command=self.toggle_default)
        self.default_disabled_bg_button.pack(pady=10)

        self.custom_disabled_bg_button = BlueButton(self, text="Custom Disabled BG", command=self.toggle_custom,
                                                    disabledbackground='#ffffff')
        self.custom_disabled_bg_button.pack(pady=10)

        self.toggle_button = tk.Button(self, text="Toggle Both Buttons State", command=self.toggle_both)
        self.toggle_button.pack(pady=20)

    def toggle_default(self):
        self.toggle_button_state(self.default_disabled_bg_button)

    def toggle_custom(self):
        self.toggle_button_state(self.custom_disabled_bg_button)

    def toggle_both(self):
        self.toggle_default()
        self.toggle_custom()

    @staticmethod
    def toggle_button_state(button):
        if button['state'] == 'normal':
            button.config(state='disabled')
        else:
            button.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("BlueButton Demo")

    demo = _BlueButtonDemo(root)

    root.mainloop()
