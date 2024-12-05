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



def remove_expense():
    selected_item = table.selection()
    if selected_item:
        for item in selected_item:
            index = table.index(item)
            name, value = expenses[index]
            table.delete(item)
            del expenses[index]
            update_balance()


def update_balance():
    global current_balance
    total_expenses = 0
    for name, expense in expenses:
        try:
            val = currency_raw(expense)
        except AttributeError:
            val = expense
        total_expenses += float(val)
    current_balance = initial_balance - total_expenses
    balance_display_label.configure(text=f"Current Balance: R$ {currency_format(current_balance)}")


def update_variables(balance, _expenses):
    global initial_balance
    global expenses
    initial_balance = balance
    expenses = _expenses
    table.delete(*table.get_children())

    for name, value in expenses:
        _spacing_v = 70 - len(f'{value}')
        if len(f'{name}') <= 3:
            _spacing_n = 66 - len(f'{name}')
        elif name == 'Not Defined':
            _spacing_n = 58
        else:
            _spacing_n = 69 - len(f'{name}')
        value_rs = 'R$ ' + f'{value}'
        table.insert("", tk.END, values=(f"{name:^{_spacing_n}}", f"{value_rs:^{_spacing_v}}"))
    update_balance()


def start_program():
    global initial_balance
    global _initial_balance_error
    try:
        balance_entry_value = balance_entry.get()
        balance_entry_value = verify_value(balance_entry_value)
        initial_balance = float(currency_raw(balance_entry_value))
    except:
        if _initial_balance_error is not None:
            _initial_balance_error.destroy()
        _initial_balance_error = ctk.CTkLabel(balance_frame, text='Enter a valid value', text_color='#d45b50')
        _initial_balance_error.pack()
        return
    current_balance = initial_balance
    balance_display_label.configure(text=f"Current Balance: R$ {currency_format(current_balance)}")
    balance_frame.pack_forget()
    table.pack(pady=10)
    button_frame.pack()


# App setup
app = ctk.CTk()
app.geometry("600x520")
app.title("Expense Tracker")

icon = ImageTk.PhotoImage(Image.open('assets/app_icon.ico'))
app.wm_iconphoto(True, icon)

# Balance input frame
balance_frame = ctk.CTkFrame(app)
balance_frame.pack(pady=200, fill='both')

balance_instruction_label = ctk.CTkLabel(balance_frame, text="Enter the Initial Balance:")
balance_instruction_label.pack()

balance_entry = ctk.CTkEntry(balance_frame)
balance_entry.pack(pady=5)

start_button = ctk.CTkButton(balance_frame, text="Start", command=start_program)
start_button.pack(pady=5)

# Label to display the current balance
balance_display_label = ctk.CTkLabel(app, text="Current Balance: R$ 0.00")
balance_display_label.pack(pady=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', '#2fa572')])

style.configure("Treeview.Heading",
                background="#3c4042",
                foreground="white",
                relief="flat")
style.map("Treeview.Heading",
          background=[('active', '#2fa572')])

table = ttk.Treeview(app, columns=("Name", "Value"))
table.heading("Name", text="Expense Name")
table.heading("Value", text="Expense Value")
table.column("#0", width=0, stretch=tk.NO)

frame = ctk.CTkFrame(app)
frame.pack(pady=10)

name_label = ctk.CTkLabel(frame, text="Expense Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ctk.CTkEntry(frame, placeholder_text='Name')
name_entry.grid(row=0, column=1, padx=5, pady=5)

value_label = ctk.CTkLabel(frame, text="Expense Value:")
value_label.grid(row=1, column=0, padx=5, pady=5)
value_entry = ctk.CTkEntry(frame, placeholder_text='Numeric Value')
value_entry.grid(row=1, column=1, padx=5, pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

add_button = ctk.CTkButton(button_frame, text="Add Expense", command=add_expense)
add_button.pack(side=tk.LEFT, padx=5)

remove_button = ctk.CTkButton(button_frame, text="Remove Expense", command=remove_expense)
remove_button.pack(side=tk.RIGHT, padx=5)

export_button = ctk.CTkButton(button_frame, text="Export", command=lambda: export(initial_balance, current_balance, expenses))
export_button.pack(padx=5)

# Modify the import button to call importer without arguments
import_button = ctk.CTkButton(button_frame, text="Import", command=lambda: update_variables(*importer()))
import_button.pack(padx=5)

app.mainloop()
