import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from functions import currency_format, currency_raw, export, importer
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

expenses = []
initial_balance = 0
current_balance = initial_balance
_initial_balance_error = None
_value_error = None


def _value_test(value):
    try:
        currency_raw(value)
        return None
    except:
        return 'string'


def verify_value(value):
    BANNED_CHARS = '$BRLUSDusdbrl '
    for char in BANNED_CHARS:
        value = value.replace(char, '')
    return value


def add_expense():
    global _value_error
    name = name_entry.get()
    value = value_entry.get()

    if name == '':
        name = 'Not Defined'

    value = verify_value(value)

    try:
        _test = _value_test(value)
        if _test is None:
            if _value_error is not None:
                _value_error.destroy()
        else:
            int(_test)
    except:
        if _value_error is not None:
            _value_error.destroy()
        _value_error = ctk.CTkLabel(frame, text='Enter a valid value!', text_color='#d45b50')
        _value_error.grid(row=1, column=3, padx=5, pady=5)
        return

    expenses.append((name, value))

    _spacing_v = 70 - len(f'{value}')
    if len(f'{name}') <= 3:
        _spacing_n = 66 - len(f'{name}')
    elif name == 'Not Defined':
        _spacing_n = 58
    else:
        _spacing_n = 69 - len(f'{name}')
    value_rs = 'R$ ' + value
    table.insert("", tk.END, values=(f"{name:^{_spacing_n}}", f"{value_rs:^{_spacing_v}}"))
    name_entry.delete(0, tk.END)
    value_entry.delete(0, tk.END)

    update_balance()


