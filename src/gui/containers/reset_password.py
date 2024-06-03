from tkinter import messagebox, ttk
import tkinter as tk

from src.gui.containers.widgets.toggle_button import ToggleButton
from src.gui.containers.frames.double_column_item_manager import DoubleColumnItemManager

class ResetPasswordWidget(tk.Frame):
    FONT_FAMILY = 'Arial'

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - Self
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # Label - Require Password
        self.require_pw_label = tk.Label(self, text='Require Password', font=(self.FONT_FAMILY, 14, 'bold'))
        self.require_pw_label.grid(row=0, column=0, sticky=tk.W, padx=0, pady=(0, 15))

        # Widget - ToggleButton
        self.require_pw_toggle = ToggleButton(self, initial_state=False)
        self.require_pw_toggle.grid(row=0, column=3, sticky=tk.E, padx=(0, 0), pady=(0, 15))

        # Label - Change Label
        self.change_pw_label = tk.Label(self, text='Change Password', font=(self.FONT_FAMILY, 12))
        self.change_pw_label.grid(row=1, column=0, pady=(0, 0), sticky=tk.SW)

        # Label - Validation Message
        self.validation_message = tk.Label(
            self, text="", fg='grey', font=(self.FONT_FAMILY, 8, 'italic'), width=35, anchor=tk.W
        )
        self.validation_message.grid(row=2, column=0, pady=(0, 0), sticky=tk.W)

        # Button - Show Password
        self.show_password_button = tk.Button(
            self,
            text='Show',
            font=(self.FONT_FAMILY, 7),
            width=4,
            command=self.toggle_password,
        )
        self.show_password_button.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.NE)

        # Label - New Password
        self.new_password_label = tk.Label(self, text='New Password', font=(self.FONT_FAMILY, 10))
        self.new_password_label.grid(row=1, column=2, sticky=tk.SW, padx=5, pady=(0, 1))

        # Entry - New Password
        self.new_password = tk.Entry(self, show='*')
        self.new_password.bind('<KeyRelease>', self.validate_password)
        self.new_password.grid(row=2, column=2, padx=5, pady=6, sticky=tk.NW)

        # Label - Confirm Password
        self.confirm_password_label = tk.Label(self, text='Confirm Password', font=(self.FONT_FAMILY, 10))
        self.confirm_password_label.grid(row=1, column=3, sticky=tk.SW, padx=(5, 0), pady=(0, 1))

        # Entry - Confirm Password
        self.confirm_password = tk.Entry(self, show='*')
        self.confirm_password.bind('<KeyRelease>', self.validate_password)
        self.confirm_password.grid(row=2, column=3, padx=(0, 0), pady=6, sticky=tk.NW)

        self.validate_password()

    def toggle_password(self):
        if self.show_password_button.config('text')[-1] == 'Show':
            self.new_password.config(show='')
            self.confirm_password.config(show='')
            self.show_password_button.config(text='Hide')
        else:
            self.new_password.config(show='*')
            self.confirm_password.config(show='*')
            self.show_password_button.config(text="Show")

    def set_show_password_button_text(self, text):
        self.show_password_button.config(text=text)

    def validate_password(self, event=None):
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        if not new_password and not confirm_password:
            self.set_validation_message('Password must be at least 7 characters.', 'grey')
        elif len(new_password) < 7:
            self.set_validation_message('Password must be at least 7 characters.', 'red')
        elif new_password != confirm_password:
            self.set_validation_message('Passwords do not match.', 'red')
        else:
            self.set_validation_message('Passwords match!', 'green')
        return new_password and confirm_password and len(new_password) >= 7 and new_password == confirm_password

    def set_validation_message(self, message, color):
        self.validation_message.config(text=message, fg=color)

    def get_require_password(self):
        return self.require_pw_toggle.state

    def get_new_password(self):
        return self.new_password.get()

    def get_confirm_password(self):
        return self.confirm_password.get()

    def is_password_valid(self):
        return self.validate_password()


class DemoApp(tk.Tk):
    def __init__(self,  parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Frame - Self
        self.title('Demo Application')
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        # Label - Title
        self.page_title = tk.Label(self, text='Secure Storage', font=('Arial', 20, 'bold'))
        self.page_title.grid(row=0, column=0, sticky=tk.W, padx=0, pady=(0, 15))

        # Separator
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=5, sticky=tk.EW, pady=10)

        # # Label - Notes
        # self.notes = tk.Label(self, text='Notes', font=('Arial', 14, 'bold'))
        # self.notes.grid(row=2, column=0, sticky=tk.W, padx=0, pady=(0, 15))

        # self.scrollable_text_area = ScrollableTextArea(self)
        # self.scrollable_text_area.grid(row=3, column=2, columnspan=3, sticky='nsew', padx=(10, 10), pady=(10, 10))

        config_double = [("Item1A", "Item1B"), ("Item2A", "Item2B"), ("Item3A", "Item3B")]
        self.item_manager_early = DoubleColumnItemManager(
            parent=self, items=config_double, item_type="Password", column_names=["Source", "Password"]
        )
        self.item_manager_early.grid(row=3, column=2, columnspan=3, sticky='nsew', padx=(10, 15), pady=(5, 10))



        # Separator
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=4, column=1, columnspan=4, sticky=tk.EW, pady=10, padx=(5, 0))

        #
        self.reset_password_widget = ResetPasswordWidget(self)
        self.reset_password_widget.grid(row=5, column=2, columnspan=3, padx=(10, 15), pady=10, sticky=tk.NSEW)

        # Separator
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=6, column=0, columnspan=5, sticky=tk.EW, pady=10)

        # Frame - Button Container
        self.b_frame = tk.Frame(self)
        self.b_frame.grid(row=7, column=4, sticky=tk.NSEW, padx=(0, 5), pady=(0, 0))

        # Button - Show State
        self.show_state_button = tk.Button(
            self.b_frame,
            text='Show State',
            width=10,
            command=self.show_state
        )
        self.show_state_button.grid(row=0, column=0, pady=(0, 10), padx=(0, 10), sticky=tk.EW)

        # Button - Preform Action
        self.perform_action_button = tk.Button(
            self.b_frame,
            text='Perform Action',
            width=10,
            command=self.perform_action_based_on_state
        )
        self.perform_action_button.grid(row=0, column=1, pady=(0, 10), padx=(0, 10), sticky=tk.EW)

        # config_double = [("Item1A", "Item1B"), ("Item2A", "Item2B"), ("Item3A", "Item3B")]
        # self.item_manager = DoubleColumnItemManager(
        #     parent=self, items=config_double, item_type="Password", column_names=["Source", "Password"]
        # )
        # self.item_manager.grid(row=2, rowspan=4, column=0, padx=(10, 10), pady=(10, 10), sticky=tk.NSEW)
        self.scrollable_text_area = ScrollableTextArea(self)
        self.scrollable_text_area.grid(row=2, rowspan=4, column=0, padx=(15, 10), pady=(5, 10), sticky=tk.NSEW)
        self.scrollable_text_area.set_text(
            "I've got a secret\n"
           "It's on the tip of my tongue,\n"
           "it's on the back of my lungs\n"
           "And I'm gonna keep it\n"
           "I know something you don't know…\n"
        )



        # Separator
        self.vertical_separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.vertical_separator.grid(row=1, rowspan=6, column=1, sticky='ns', padx=(5, 5), pady=(10, 11))

        # # Separator
        # self.vertical_separator = ttk.Separator(self, orient=tk.VERTICAL)
        # self.vertical_separator.grid(row=1, rowspan=6, column=5, sticky='ns', padx=(5, 5), pady=(15, 5))

        configure_styles()
        initialize_icons()

    def show_state(self):
        require_password = self.reset_password_widget.get_require_password()
        new_password = self.reset_password_widget.get_new_password()
        confirm_password = self.reset_password_widget.get_confirm_password()
        password_valid = self.reset_password_widget.is_password_valid()

        state_message = (
            f'Require Password: {'Yes' if require_password else 'No'}\n'
            f'New Password: {new_password}\n'
            f'Confirm Password: {confirm_password}\n'
            f'Password Valid: {'Yes' if password_valid else 'No'}'
        )
        messagebox.showinfo('Current State', state_message)

    def perform_action_based_on_state(self):
        require_password = self.reset_password_widget.get_require_password()
        password_valid = self.reset_password_widget.is_password_valid()

        if require_password and password_valid:
            messagebox.showinfo('Action', 'Password requirement is enabled and passwords are valid.')
        elif require_password:
            messagebox.showwarning('Action', 'Password requirement is enabled, but passwords are invalid.')
        else:
            messagebox.showinfo('Action', 'Password requirement is disabled.')


if __name__ == '__main__':
    from src.gui.containers.widgets.scrollable_text_area import ScrollableTextArea
    from src.application_config.icon_setup import initialize_icons
    from src.gui.styles import configure_styles


    app = DemoApp()
    app.mainloop()
