
import tkinter as tk
from tkinter import ttk
from src.constants import Colors


def configure_styles():
    style = ttk.Style()
    blue_button_style(style)
    blue_combo_style(style)
    treeview_style(style)


def blue_button_style(style: ttk.Style) -> ttk.Style:
    style.configure(
        style='Blue.TButton',
        background=Colors.CAVOLO_NERO,
        foreground=Colors.BLACK,
        borderwidth=2,
        relief='raised',
        padding=4,
        anchor='center',
        width=20,
    )
    style.map(
        style='Blue.TButton',
        background=[
            ('active', '!pressed', Colors.ADRIFT),
            ('active', 'pressed', Colors.ADRIFT_BRIGHT),
            ('disabled', Colors.BLUE_GRAY_BRIGHT),
        ],
        foreground=[
            ('active', '!pressed', Colors.BLUE_GRAY_DARK),
            ('active', 'pressed', Colors.BLUE_GRAY_DESATURATE),
            ('disabled', Colors.BLUE_GRAY_DESATURATE),
        ],
        relief=[
            ('active', 'pressed', tk.RIDGE),
            ('active', '!pressed', tk.RAISED),
            ('disabled', tk.RAISED),
        ],
    )
    return style


def blue_combo_style(style: ttk.Style) -> ttk.Style:
    style_name = "Blue.TCombobox"

    style.configure(
        style=style_name,
        fieldbackground=Colors.BLUE_GRAY_BRIGHT,  # Background of the entry field
        background=Colors.BLUE_GRAY_BRIGHT,       # Background of the dropdown list
        foreground=Colors.BLUE_GRAY_DARK,         # Text color
        relief=tk.GROOVE,
        arrowsize=15,
        borderwidth=4,
        width=1,
        selectbackground=Colors.BLUE_GRAY_BRIGHT,
        selectforeground=Colors.BLUE_GRAY_DARK,
    )
    style.map(
        style=style_name,
        fieldbackground=[
            ('readonly', Colors.BLUE_GRAY_BRIGHT),
            ('!readonly', 'white')
        ],
        background=[
            ('readonly', Colors.BLUE_GRAY_BRIGHT),
            ('!readonly', 'white')
        ],
        foreground=[
            ('readonly', Colors.BLUE_GRAY_DARK),
            ('!readonly', Colors.BLUE_GRAY_DARK)
        ],
        relief=[
            ('pressed', 'sunken'),
            ('!pressed', 'groove')
        ],
        arrowcolor=[
            ('active', Colors.BLUE_GRAY),
            ('!active', Colors.BLUE_GRAY_DARK)
        ]
    )

    return style


def treeview_style(style: ttk.Style) -> ttk.Style:
    # Treeview - Base
    style.configure(
        style="Treeview",
        font=("Helvetica", 12),
        rowheight=25,
        fieldbackground=Colors.SNOWFLAKE,
        background=Colors.SNOWFLAKE
    )
    style.map(
        style='Treeview',
        background=[
            ('selected', Colors.CONCRETE)
        ],
        foreground=[
            ('selected', Colors.HEART_POTION)
        ]
    )
    style.layout(
        "Treeview",
        [
            ('Treeview.treearea', {'sticky': tk.NSEW})
        ]
    )

    # Treeview - Heading
    style.configure(
        style="Treeview.Heading",
        font=("Helvetica", 12, "bold"),
        foreground=Colors.CARBON,
        background=Colors.BLUE_GRAY
    )
    style.map(
        style="Treeview.Heading",
        background=[
            ('!active', Colors.BLUE_GRAY),
            ('active', Colors.BLUE_GRAY)
        ],
        foreground=[
            ('!active', Colors.CARBON),
            ('active', Colors.CARBON)
        ]
    )

    # Treeview - Scrollbar
    style.configure(
        style="Vertical.TScrollbar",
        gripcount=0,
        background=Colors.BLUE_GRAY,
        darkcolor=Colors.BLUE_GRAY,
        lightcolor=Colors.BLUE_GRAY,
        troughcolor=Colors.ORBITAL,
        bordercolor=Colors.BLUE_GRAY,
        arrowcolor=Colors.HEART_POTION
    )
    style.map(
        style="Vertical.TScrollbar",
        background=[
            ('active', Colors.ORBITAL),
            ('!active', Colors.ORBITAL)
                    ],
        troughcolor=[
            ('active', Colors.ORBITAL),
            ('!active', Colors.BLUE_GRAY)
        ],
        arrowcolor=[
            ('active', Colors.HEART_POTION),
            ('!active', Colors.CARBON)
        ]
    )

    return style
