import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import tempfile
import subprocess
import sys
from typing import List


class IPManagerWidget:
    def __init__(self, master, row, current_ip):
        self.master = master
        self.current_ip = current_ip.split('.')
        self.octets = []
        ip_frame = tk.Frame(master)
        tk.Label(master, text="IP Address:").grid(row=row, column=1, padx=10, pady=10, sticky='w')
        ip_frame.grid(row=row, column=1, padx=10, pady=10, sticky='e')

        for i in range(4):
            octet = OctetWidget(ip_frame, self.advance_focus, i, self.current_ip[i])
            if i < 3:
                tk.Label(ip_frame, text=".").pack(side=tk.LEFT)
            octet.pack()
            self.octets.append(octet)

        self.set_button = tk.Button(master, text="Set", command=self.set_ip_address)
        self.set_button.grid(row=row, column=2, padx=10, pady=10, sticky='EW')
        manage_button = tk.Button(master, text="Manage", command=self.manage_ip_settings)
        manage_button.grid(row=row, column=3, padx=10, pady=10, sticky='EW')

    def advance_focus(self, index):
        if index < len(self.octets):
            self.octets[index].entry.focus()
        else:
            self.set_button.focus()

    def set_ip_address(self) -> None:
        ip_address = '.'.join(part.get() for part in self.ip_parts)
        print("Setting IP Address:", ip_address)

    def manage_ip_settings(self) -> None:
        manage_window = tk.Toplevel(self.master)
        manage_window.title("IP Settings")
        tk.Label(manage_window, text="IP Settings Management").pack()

    def validate_ip_part(self, P: str) -> bool:
        if P == "":
            return True
        if P.isdigit():
            num = int(P)
            return 0 < num < 255
        return False

    def get_current_ip(self) -> str:
        return '192.168.1.100'


class OctetWidget:
    def __init__(self, master, advance_callback, index, initial_value=''):
        self.master = master
        self.advance_callback = advance_callback
        self.index = index
        self.entry = tk.Entry(master, width=3, justify='center')
        self.entry.insert(0, initial_value)
        self.entry.bind('<KeyPress>', self.handle_key_press)
        self.entry.bind('<FocusOut>', self.handle_focus_out)
        self.entry.bind('<Button-1>', self.handle_click)
        self.original_value = initial_value  # Keep track of the original value for restoration

    def handle_key_press(self, event):
        if event.char.isdigit():
            if self.is_valid_digit_addition(event.char):
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.entry.get() + event.char)
                self.check_advance_conditions()
                return "break"
        elif event.keysym in ['period', 'Return']:
            self.advance_callback(self.index + 1)
            return "break"
        elif event.keysym == 'BackSpace':
            if not self.entry.get():
                self.advance_callback(self.index - 1)

    def handle_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.original_value)

    def handle_click(self, event):
        self.entry.delete(0, tk.END)

    def is_valid_digit_addition(self, char):
        potential_value = int(self.entry.get() + char)
        return 0 < potential_value <= 254

    def check_advance_conditions(self):
        current_value = self.entry.get()
        if len(current_value) == 3 or not self.can_add_digit(current_value):
            self.advance_callback(self.index + 1)

    def can_add_digit(self, current_value):
        if len(current_value) == 2:
            potential_value = int(current_value + '9')
            return 0 < potential_value <= 254
        return True

    def pack(self, side=tk.LEFT):
        self.entry.pack(side=side)
