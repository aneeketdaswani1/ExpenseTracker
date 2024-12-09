import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class ExpenseManager:
    def __init__(self):
        self.initial_balance = 0
        self.current_balance = 0
        self.expenses = []
        self.export_app = None
        self.archivename_entry = None

    @staticmethod
    def currency_format(value):
        try:
            formatted_value = '{:_.2f}'.format(float(value)).replace('.', ',').replace('_', '.')
            return formatted_value
        except (ValueError, TypeError):
            return "Invalid Value"

    @staticmethod
    def currency_raw(value):
        try:
            value = value.replace('$', '').replace('.', '').replace(',', '.')
            return float(value)
        except ValueError:
            return None

    def export_values(self,initial_bal, current_bal, exp):
        self.initial_balance = initial_bal
        self.current_balance = current_bal
        self.expenses = exp

    def export_screen(self):
        self.export_app = ctk.CTk()
        self.export_app.geometry("500x300")  # Increased size for better visibility
        self.export_app.title("Export")

        export_frame = ctk.CTkFrame(self.export_app)
        export_frame.pack(pady=20, fill="both", expand=True)

        # File name entry label and input
        ctk.CTkLabel(export_frame, text="File name (optional)", font=("Arial", 16)).pack(pady=5)
        self.archivename_entry = ctk.CTkEntry(export_frame, font=("Arial", 14))
        self.archivename_entry.pack(pady=5)

        # Export option label
        ctk.CTkLabel(export_frame, text="Choose an export option", font=("Arial", 16)).pack(pady=5)

        # Frame for the export buttons
        button_frame = ctk.CTkFrame(export_frame)
        button_frame.pack(pady=10)

        # Export buttons
        excel_button = ctk.CTkButton(button_frame, text="Excel", font=("Arial", 14), command=self.export_excel1)
        excel_button.pack(pady=5, padx=10, side="left")

        pdf_button = ctk.CTkButton(button_frame, text="PDF", font=("Arial", 14), command=self.export_pdf1)
        pdf_button.pack(pady=5, padx=10, side="left")

        # Cancel button to close the export popup
        cancel_button = ctk.CTkButton(
            export_frame, 
            text="Cancel", 
            font=("Arial", 14), 
            fg_color="#E57373", 
            command=self.export_app.destroy
        )
        cancel_button.pack(pady=20)

        self.export_app.mainloop()


    @staticmethod
    def show_success_popup(message):
        popup = ctk.CTkToplevel()
        popup.geometry("300x150")
        popup.title("Success")
        popup.grab_set()
        ctk.CTkLabel(popup, text=message, font=("Arial", 16)).pack(pady=20)
        popup.after(1000, popup.destroy)

    def export_pdf1(self):
        file_name = self.archivename_entry.get() or 'Expense Control'
        self.export_app.withdraw()
        folder_path = filedialog.askdirectory(title='Choose a folder')
        self.export_app.deiconify()

        if not folder_path:
            return

        pdf_path = os.path.join(folder_path, f'{file_name}.pdf')
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
        elements = []
        styles = getSampleStyleSheet()

        try:
            initial_formatted = self.currency_format(self.initial_balance)
            current_formatted = self.currency_format(self.current_balance)
            diff_formatted = self.currency_format(self.initial_balance - self.current_balance)
        except Exception as e:
            print(f"Error formatting balances: {e}")
            return

        balance_data = [[
            Paragraph(f'Initial Balance: R$ {initial_formatted}', styles['Normal']),
            Paragraph(f'Total Expenses: R$ -{diff_formatted}', styles['Normal']),
            Paragraph(f'Final Balance: R$ {current_formatted}', styles['Normal']),
        ]]

        balance_table = Table(balance_data, colWidths=[pdf.width / 3] * 3)
        balance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(balance_table)
        elements.append(Spacer(1, 12))

        data = [['Expense', 'Amount']] + [
            [name, f'R$ {self.currency_format(value)}'] for name, value in self.expenses
        ]
        table = Table(data, colWidths=[pdf.width / len(data[0])] * len(data[0]))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        pdf.build(elements)

        self.export_app.destroy()
        self.show_success_popup("Exported successfully!")

    def export_excel1(self):
        file_name = self.archivename_entry.get() or 'Expense Control'
        self.export_app.withdraw()
        folder_path = filedialog.askdirectory(title='Choose a folder')
        self.export_app.deiconify()

        if not folder_path:
            return

        excel_path = os.path.join(folder_path, f'{file_name}.xlsx')
        data = []
        balance = self.initial_balance
        for name, value in self.expenses:
            data.append({
                'Balance': f'$ {self.currency_format(balance)}',
                'Expense': name,
                'Expense Amount': f'$ {self.currency_format(value)}',
            })
            balance -= float(value)

        pd.DataFrame(data).to_excel(excel_path, index=False, engine='openpyxl')
        self.export_app.destroy()
        self.show_success_popup("Exported successfully!")

    def import_values(self):
        print("Here in import values ")
        try:
            file_path = filedialog.askopenfilename(
                title='Choose a file',
                filetypes=[('Excel Files', '*.xlsx')]
            )

            if not file_path:
                print("No file selected.")
                return None

            # Read the Excel file using pandas
            imported_df = pd.read_excel(file_path, engine='openpyxl')

            # Check if 'Balance' and expected columns are present
            required_columns = {'Balance', 'Expense', 'Expense Amount'}
            if not required_columns.issubset(imported_df.columns):
                print(f"Error: Missing required columns. Expected columns: {required_columns}")
                return None

            # Extract initial balance (assuming it is in the first row)
            initial_balance_str = imported_df.loc[0, 'Balance']  # Assuming the balance is in the first row
            initial_balance = self.currency_raw(initial_balance_str)

            if initial_balance is None:
                print("Error: Invalid balance value")
                return None

            # Extract expenses from the DataFrame
            expenses = []
            for _, row in imported_df.iterrows():
                expense_name = row['Expense']
                expense_amount_str = row['Expense Amount']

                if pd.notna(expense_name) and pd.notna(expense_amount_str):
                    expense_amount = self.currency_raw(expense_amount_str)
                    if expense_amount is not None:
                        expenses.append((expense_name, expense_amount))
                    else:
                        print(f"Error: Invalid expense amount '{expense_amount_str}' for expense '{expense_name}'")

            print(f"File successfully imported. Initial balance: {initial_balance}, Expenses: {len(expenses)} items.")
            return initial_balance, expenses

        except Exception as e:
            print(f"Error importing Excel file: {e}")
            return None
