import tkinter as tk
from tkinter import ttk, simpledialog
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
_update_window = None


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
        _value_error = ctk.CTkLabel(frame, text='Enter a valid value!', text_color='#d45b50', font=("Arial", 12))
        _value_error.grid(row=1, column=3, padx=5, pady=5)
        return

    expenses.append((name, value))

    value_rs = '$' + value
    table.insert("", tk.END, values=(name, value_rs))
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


def update_expense():
    global _update_window
    selected_item = table.selection()
    if selected_item:
        # Get the selected item's index in the expenses list
        index = table.index(selected_item[0])
        current_name, current_value = expenses[index]

        # Close any existing update window
        if _update_window and _update_window.winfo_exists():
            _update_window.destroy()

        # Create a new update window
        _update_window = ctk.CTkToplevel(app)
        _update_window.title("Update Expense")
        _update_window.geometry("400x250")
        _update_window.attributes('-topmost', True)

        # Name update section
        name_update_label = ctk.CTkLabel(_update_window, text="Expense Name:", font=("Arial", 14))
        name_update_label.pack(pady=(20, 5))
        name_update_entry = ctk.CTkEntry(_update_window, font=("Arial", 14), 
                                         placeholder_text="Enter new name")
        name_update_entry.insert(0, current_name)
        name_update_entry.pack(pady=5)

        # Value update section
        value_update_label = ctk.CTkLabel(_update_window, text="Expense Value:", font=("Arial", 14))
        value_update_label.pack(pady=(10, 5))
        value_update_entry = ctk.CTkEntry(_update_window, font=("Arial", 14), 
                                          placeholder_text="Enter new value")
        value_update_entry.insert(0, current_value.replace('$', ''))
        value_update_entry.pack(pady=5)

        def save_update():
            # Validate and save the updated expense
            new_name = name_update_entry.get()
            new_value = value_update_entry.get()

            # Verify and clean the value
            new_value = verify_value(new_value)

            # Validate the new value
            try:
                _test = _value_test(new_value)
                if _test is not None:
                    int(_test)
            except:
                # Show error if value is invalid
                error_label = ctk.CTkLabel(_update_window, text='Enter a valid value!', 
                                           text_color='#d45b50', font=("Arial", 12))
                error_label.pack(pady=5)
                return

            # Update the expenses list
            expenses[index] = (new_name, new_value)

            # Update the table
            value_rs = '$' + new_value
            table.item(selected_item[0], values=(new_name, value_rs))

            # Update balance
            update_balance()

            # Close the update window
            _update_window.destroy()

        # Save button
        save_button = ctk.CTkButton(_update_window, text="Save", 
                                    command=save_update, 
                                    font=("Arial", 14))
        save_button.pack(pady=20)


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
    balance_display_label.configure(text=f"Current Balance: ${currency_format(current_balance)}")


def update_variables(balance, _expenses):
    global initial_balance
    global expenses
    initial_balance = balance
    expenses = _expenses
    table.delete(*table.get_children())

    for name, value in expenses:
        value_rs = '$' + f'{value}'
        table.insert("", tk.END, values=(name, value_rs))
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
        _initial_balance_error = ctk.CTkLabel(balance_frame, text='Enter a valid value', text_color='#d45b50', font=("Arial", 12))
        _initial_balance_error.pack()
        return
    current_balance = initial_balance
    balance_display_label.configure(text=f"Current Balance: $ {currency_format(current_balance)}")
    balance_frame.pack_forget()
    table_frame.pack(pady=10, padx=20, fill='x')
    button_frame.pack()


# App setup
app = ctk.CTk()
app.geometry("650x520")
app.title("Expense Tracker")

icon = ImageTk.PhotoImage(Image.open('assets/app_icon.ico'))
app.wm_iconphoto(True, icon)

# Balance input frame
balance_frame = ctk.CTkFrame(app)
balance_frame.pack(pady=200, fill='both')

balance_instruction_label = ctk.CTkLabel(balance_frame, text="Enter the Initial Balance:", font=("Arial", 14))
balance_instruction_label.pack()

balance_entry = ctk.CTkEntry(balance_frame, font=("Arial", 14))
balance_entry.pack(pady=5)

start_button = ctk.CTkButton(balance_frame, text="Start", command=start_program, font=("Arial", 14))
start_button.pack(pady=5)

# Label to display the current balance
balance_display_label = ctk.CTkLabel(app, text="Current Balance: $0.00", font=("Arial", 16))
balance_display_label.pack(pady=10)

# Style adjustments for Treeview (Expense List)
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=30,
                fieldbackground="#343638",
                font=("Arial", 14),
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', '#2fa572')])

style.configure("Treeview.Heading",
                background="#3c4042",
                foreground="white",
                relief="flat",
                font=("Arial", 14))
style.map("Treeview.Heading",
          background=[('active', '#2fa572')])

# Treeview (Expense List)
table_frame = ctk.CTkFrame(app, width=550)
table_frame.pack_forget()

table = ttk.Treeview(table_frame, columns=("Name", "Value"), show="headings", height=10)
table.heading("Name", text="Expense Name")
table.heading("Value", text="Expense Value")

# Adjust column alignment and widths
table.column("Name", anchor="center", width=300)
table.column("Value", anchor="center", width=200)
table.column("#0", width=0, stretch=tk.NO)

table.pack(fill='both', expand=True)

# Bind double-click event to update_expense function
table.bind('<Double-1>', lambda event: update_expense())

# Input Frame for Expenses
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

name_label = ctk.CTkLabel(frame, text="Expense Name:", font=("Arial", 14))
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ctk.CTkEntry(frame, placeholder_text='Name', font=("Arial", 14))
name_entry.grid(row=0, column=1, padx=5, pady=5)

value_label = ctk.CTkLabel(frame, text="Expense Value:", font=("Arial", 14))
value_label.grid(row=1, column=0, padx=5, pady=5)
value_entry = ctk.CTkEntry(frame, placeholder_text='Numeric Value', font=("Arial", 14))
value_entry.grid(row=1, column=1, padx=5, pady=5)

# Button Frame
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

add_button = ctk.CTkButton(button_frame, text="Add Expense", command=add_expense, font=("Arial", 14))
add_button.pack(side=tk.LEFT, padx=5)

remove_button = ctk.CTkButton(button_frame, text="Remove Expense", command=remove_expense, font=("Arial", 14))
remove_button.pack(side=tk.RIGHT, padx=5)

# Add Update button
update_button = ctk.CTkButton(button_frame, text="Update Expense", command=update_expense, font=("Arial", 14))
update_button.pack(padx=5)

export_button = ctk.CTkButton(button_frame, text="Export", command=lambda: export(initial_balance, current_balance, expenses), font=("Arial", 14))
export_button.pack(padx=5)

import_button = ctk.CTkButton(button_frame, text="Import", command=lambda: update_variables(*importer()), font=("Arial", 14))
import_button.pack(padx=5)

app.mainloop()