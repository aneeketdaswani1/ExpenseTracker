import customtkinter as ctk
from tkinter import ttk, messagebox,simpledialog
from functions import Functions 
from exporter import ExpenseManager

import tkinter.font as tkfont
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from PIL import Image ,ImageTk


class ExpenseTracker:
    def __init__(self):
        # Initialize the main app window
        self.app = ctk.CTk()
        self.app.geometry("1100x800")
        self.app.title("Expense Tracker")
        self.app.configure(fg_color="#2E3B55")  # Set background color

        self.f = Functions()
        self.ex = ExpenseManager()
        # Variables
        self.expenses = []
        self.initial_balance = 0
        self.current_balance = 0
        style = ttk.Style()
        default_font = tkfont.nametofont("TkDefaultFont")  # Get the default font

        # Configure style for the Treeview
        style.configure(
            "Treeview",
            font=(default_font.actual("family"), 14),  # Set font size (e.g., 14)
            rowheight=30  # Adjust row height for larger font
        )
        style.configure(
            "Treeview.Heading",
            font=(default_font.actual("family"), 16, "bold")  # Larger and bold font for headers
        )

        # Setup styles and create widgets
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.create_widgets()
        self.show_start_frame()

    def create_widgets(self):
            # Fonts and Colors
        self.header_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 16)
        self.button_font = ("Arial", 16)

        # Start Frame
        self.start_frame = ctk.CTkFrame(self.app)
        ctk.CTkLabel(
            self.start_frame,
            text="Welcome to Expense Tracker",
            font=self.header_font,
            text_color="white",
        ).place(relx=0.5, rely=0.3, anchor="center")  # Centered

        # Buttons
        ctk.CTkButton(
            self.start_frame,
            text="Create New File",
            font=self.button_font,
            fg_color="#4CAF50",
            text_color="white",
            width=300,
            command=self.show_create_file,
        ).place(relx=0.5, rely=0.5, anchor="center")  # Centered below the label

        ctk.CTkButton(
            self.start_frame,
            text="Import File",
            font=self.button_font,
            fg_color="#2196F3",
            text_color="white",
            width=300,
            command=self.show_import_file,
        ).place(relx=0.5, rely=0.6, anchor="center")  # Centered below the first button


        # Balance Input Frame
        self.balance_frame = ctk.CTkFrame(self.app)
        ctk.CTkLabel(
            self.balance_frame,
            text="Enter Initial Balance",
            font=self.header_font,
            text_color="white",
        ).place(relx=0.5, rely=0.4, anchor="center")  # Centered

        # Entry
        self.balance_entry = ctk.CTkEntry(
            self.balance_frame, 
            font=self.label_font, 
            placeholder_text="Enter Amount"
        )
        self.balance_entry.place(relx=0.5, rely=0.5, anchor="center")  # Centered below the label

        # Button
        ctk.CTkButton(
            self.balance_frame,
            text="Start",
            font=self.button_font,
            fg_color="#4CAF50",
            width=300,
            command=self.start_program,
        ).place(relx=0.5, rely=0.6, anchor="center") 
        # Expense Table Frame
        self.table_frame = ctk.CTkFrame(self.app)
        self.expense_table = ttk.Treeview(
            self.table_frame, columns=("Name", "Value"), show="headings", height=10 
        )
        self.expense_table.heading("Name", text="Expense Name")
        self.expense_table.heading("Value", text="Expense Value")
        self.expense_table.column("Name", anchor="center", width=300)
        self.expense_table.column("Value", anchor="center", width=200)
        self.expense_table.pack(fill="both", expand=True)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self.app)
        ctk.CTkLabel(
            self.input_frame, text="Expense Name:", font=self.label_font
        ).grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(self.input_frame, font=self.label_font, placeholder_text="Enter name")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(
            self.input_frame, text="Expense Value:", font=self.label_font
        ).grid(row=1, column=0, padx=10, pady=5)
        self.value_entry = ctk.CTkEntry(self.input_frame, font=self.label_font, placeholder_text="Enter value")
        self.value_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons for Actions
        self.button_frame = ctk.CTkFrame(self.app)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        # Place buttons dynamically based on the available width
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Expense",
            font=self.button_font,
            width=200,
            command=self.add_expense,
        )
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Remove Expense",
            font=self.button_font,
            fg_color="#E57373",
            width=200,
            command=self.remove_expense,
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Export Data",
            font=self.button_font,
            fg_color="#FFD54F",
            text_color="black",
            width=200,
            command=self.export_data,
        ).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Update Expense",
            font=self.button_font,
            fg_color="#FFB74D",
            text_color="black",
            width=200,
            command=self.update_expense,
        ).grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Go Back",
            font=self.button_font,
            fg_color="#6C7A89",
            width=200,
            command=self.show_start_frame,
        ).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Predict Future Expense",
            font=self.button_font,
            fg_color="#FF7043",
            text_color="white",
            width=200,
            command=self.show_prediction_screen,
        ).grid(row=1, column=2, padx=10, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Update Initial Balance",
            font=self.button_font,
            fg_color="#4CAF50",
            text_color="white",
            width=200,
            command=self.update_initial_balance,
        ).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Balance Display
        self.balance_display_label = ctk.CTkLabel(
            self.app,
            text="Current Balance: $0.00",
            font=self.header_font,
            text_color="white",
        )

    def update_initial_balance(self):
        """Prompts the user for a new initial balance and updates it."""
        try:
        # Show a popup dialog to ask for a new balance
            new_balance = simpledialog.askfloat(
                "Update Initial Balance",
                "Enter the new initial balance:",
                parent=self.app,
            )
            if new_balance is None:  # User cancelled the input
                return 

            # Update the initial balance and recalculate
            self.initial_balance = new_balance
            self.update_balance()
            messagebox.showinfo("Success", "Initial balance updated successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value.")
        
    
    def show_start_frame(self):
        self.clear_frames()
        self.start_frame.pack(fill="both", expand=True)

    def show_create_file(self):
        self.clear_frames()
        self.balance_frame.pack(fill="both", expand=True)

    def show_import_file(self):
        try:
            self.clear_frames()
            imported_data = self.f.importer(self.ex)
            if imported_data:
                self.update_variables(*imported_data)
                self.show_main_view()
            else:
                self.show_start_frame()
        except Exception as e:
            self.show_start_frame()

    def start_program(self):
        try:
            balance_entry_value = self.balance_entry.get()
            self.initial_balance = float(self.f.currency_raw(balance_entry_value))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric balance.")
            return
        self.current_balance = self.initial_balance
        self.update_balance_display()
        self.show_main_view()

    def add_expense(self):
        name = self.name_entry.get() or "Not Defined"
        value = self.value_entry.get()
        try:
            # Parse the value as a float and format it properly
            value = float(self.f.currency_raw(value))
            formatted_value = f"${value:,.2f}"  # Correctly format the value as currency
            self.expenses.append((name, value))
            self.update_balance()

            # Insert formatted value into the expense table
            self.expense_table.insert("", "end", values=(name, formatted_value))
            self.name_entry.delete(0, "end")
            self.value_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value.")

    def remove_expense(self):
        selected_items = self.expense_table.selection()
        for item in selected_items:
            index = self.expense_table.index(item)
            self.expense_table.delete(item)
            del self.expenses[index]
        self.update_balance()
  



    def update_balance(self):
        total_expenses = sum(float(value) for _, value in self.expenses)
        self.current_balance = self.initial_balance - total_expenses
        self.update_balance_display()

    def update_balance_display(self):
        # Format the current balance properly as currency
        formatted_balance = f"${self.current_balance:,.2f}"
        self.balance_display_label.configure(text=f"Current Balance: {formatted_balance}")

    def export_data(self):
        self.f.export(self.ex,self.initial_balance, self.current_balance, self.expenses)

    def show_main_view(self):
        self.clear_frames()
        self.table_frame.pack(fill="both", padx=20, pady=10, expand=True)
        self.input_frame.pack(fill="x", padx=20, pady=10)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        self.balance_display_label.pack(pady=10)

    def update_variables(self, balance, expenses):
        self.initial_balance = balance
        self.expenses = expenses
        self.expense_table.delete(*self.expense_table.get_children())
        for name, value in self.expenses:
            self.expense_table.insert("", "end", values=(name, f"${self.f.currency_format(value)}"))
        self.update_balance()

    def clear_frames(self):
        for widget in self.app.winfo_children():
            widget.pack_forget()

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    ExpenseTracker().run()
