import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

initial_balance, current_balance, expenses = 0, 0, []

def currency_format(value):
    """
    Formats the value to the Brazilian currency standard.

    Parameters:
    - value (float or str): Value to be formatted.

    Returns:
    - str: Formatted value.
    """
    try:
        # Ensure the value is a float or convertible to float
        formatted_value = '{:_.2f}'.format(float(value)).replace('.', ',').replace('_', '.')
        return formatted_value
    except (ValueError, TypeError) as e:
        print(f"Error formatting value: {value}. Error: {e}")
        return "Invalid Value"

def currency_raw(value):
    """
    Converts the value to the Python default float format.

    Parameters:
    - value (str): Value to be converted.

    Returns:
    - float: Converted value.
    """
    try:
        # Remove currency symbols and thousand separators
        value = value.replace('$', '').replace('.', '').replace(',', '.')
        return float(value)
    except ValueError:
        return None  

def export_values(initial_bal, current_bal, exp):
    """
    Saves values for export (transfer between files).

    Parameters:
    - initial_bal (float): Initial balance.
    - current_bal (float): Current balance.
    - exp (list): List of expenses.
    """
    global initial_balance, current_balance, expenses
    initial_balance, current_balance, expenses = initial_bal, current_bal, exp

def export_screen():
    """
    Creates a file export screen.

    Returns:
    - Screen (CTk): Export screen.
    """
    global exp_app
    exp_app = ctk.CTk()
    exp_app.geometry("480x260")
    exp_app.title("Export")

    export_frame = ctk.CTkFrame(exp_app)
    export_frame.pack(pady=55, anchor='center')

    archivename_label = ctk.CTkLabel(export_frame, text="File name (optional)")
    archivename_label.pack(pady=5)

    global archivename_entry
    archivename_entry = ctk.CTkEntry(export_frame)
    archivename_entry.pack(pady=5)

    text_label = ctk.CTkLabel(export_frame, text="Choose an export option")
    text_label.pack(pady=5)

    excel_button = ctk.CTkButton(export_frame, text="Excel", command=lambda: export_excel(initial_balance, current_balance, expenses))
    excel_button.pack(pady=5, padx=5, side='left')

    none_button = ctk.CTkButton(export_frame, text="None", command=lambda: export_none(initial_balance, current_balance, expenses))
    none_button.pack(pady=5, padx=5, side='right')

    pdf_button = ctk.CTkButton(export_frame, text="PDF", command=lambda: export_pdf(initial_balance, current_balance, expenses))
    pdf_button.pack(pady=5, padx=5, side='right')

    exp_app.mainloop()

# PDF Export
def export_pdf(initial_balance, current_balance, expenses):
    """
    Creates a PDF file with balance and expense data.

    Parameters:
    - initial_balance (float): Initial balance.
    - current_balance (float): Current balance.
    - expenses (list): List of expenses.
    """
    print(f"Debugging: initial_balance = {initial_balance}, current_balance = {current_balance}, expenses = {expenses}")

    # Ensure 'file_name' is defined
    file_name = archivename_entry.get()  # Get the file name from the entry widget
    if file_name == '':
        file_name = 'Expense Control'  # Default name if no entry provided

    exp_app.withdraw()
    folder_path = filedialog.askdirectory(title='Choose a folder')
    exp_app.deiconify()

    try:
        pdf_path = os.path.join(folder_path, f'{file_name}.pdf')
    except TypeError:
        return None

    pdf = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    styles = getSampleStyleSheet()

    # Validate and format the balances
    try:
        initial_formatted = currency_format(initial_balance)
        current_formatted = currency_format(current_balance)
        diff_formatted = currency_format(initial_balance - current_balance)
    except Exception as e:
        print(f"Error formatting balances: {e}")
        return None

    balance_data = [[
        Paragraph(f'Initial Balance: R$ {initial_formatted}', styles['Normal']),
        Paragraph(f'Total Expenses: R$ -{diff_formatted}', styles['Normal']),
        Paragraph(f'Final Balance: R$ {current_formatted}', styles['Normal']),
    ]]

    balance_style = TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    balance_table = Table(balance_data, colWidths=[pdf.width / 3] * 3)
    balance_table.setStyle(balance_style)
    elements.append(balance_table)

    elements.append(Spacer(1, 12))

    # Table for expenses
    data = [['Expense', 'Amount']]
    
    for name, value in expenses:
        try:
            formatted_value = currency_format(value)
        except (ValueError, TypeError):
            formatted_value = "Invalid Value"
        data.append([name, f'R$ {formatted_value}'])

    table_style = TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table = Table(data, colWidths=[pdf.width / len(data[0])] * len(data[0]))
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)


# Excel Export
def export_excel(initial_balance, current_balance, expenses):
    """
    Creates an Excel file with balance and expense data.

    Parameters:
    - initial_balance (float): Initial balance.
    - current_balance (float): Current balance.
    - expenses (list): List of expenses.
    """
    file_name = archivename_entry.get()

    if file_name == '':
        file_name = 'Expense Control'

    exp_app.withdraw()
    folder_path = filedialog.askdirectory(title='Choose a folder')
    exp_app.deiconify()

    try:
        excel_path = os.path.join(folder_path, f'{file_name}.xlsx')
    except TypeError:
        return None

    data = []
    balance = initial_balance
    for name, value in expenses:
        row = {
            'Balance': f'R$ {currency_format(balance)}',
            'Expense': name,
            'Expense Amount': f'R$ {currency_format(value)}',
        }
        balance -= float(value) 
        data.append(row)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False, engine='openpyxl')

def export_none(initial_balance, current_balance, expenses):
    """
    Placeholder for no action.
    """
    print("No export performed.")

# Import Values
def import_values():
    """
    Imports data from a previously exported Excel file.

    Returns:
    - initial_balance (float): Initial balance.
    - expense_list (list): List of expenses.
    """
    try:
        # Open file dialog to select the Excel file
        file_path = filedialog.askopenfilename(
            title='Choose a file',
            filetypes=[('Excel Files', '*.xlsx')]
        )

        if not file_path:
            return None

        # Read the Excel file using pandas
        imported_df = pd.read_excel(file_path, engine='openpyxl')

        # Debug: Print DataFrame content to check its structure
        print("Dataframe loaded:")
        print(imported_df)

        # Check if 'Balance' and expected columns are present
        if 'Balance' not in imported_df.columns or 'Expense' not in imported_df.columns or 'Expense Amount' not in imported_df.columns:
            print("Error: Missing required columns in the file")
            return None

        # Extract initial balance (assuming it is in the second row)
        initial_balance_str = imported_df.loc[0, 'Balance']  # Assuming the balance is in the first row
        initial_balance = currency_raw(initial_balance_str)

        if initial_balance is None:
            print("Error: Invalid balance value")
            return None

        # Extract expenses from the DataFrame
        expenses = []
        for _, row in imported_df.iterrows():
            expense_name = row['Expense']
            expense_amount_str = row['Expense Amount']
            
            if pd.notna(expense_name) and pd.notna(expense_amount_str):
                expense_amount = currency_raw(expense_amount_str)
                if expense_amount is not None:
                    expenses.append((expense_name, expense_amount))
                else:
                    print(f"Error: Invalid expense amount '{expense_amount_str}' for expense '{expense_name}'")

        return initial_balance, expenses

    except Exception as e:
        print(f"Error importing Excel file: {e}")
        return None