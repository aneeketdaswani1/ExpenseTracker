import pytest
from functions import Functions
from exporter import ExpenseManager
import pandas as pd
import os
import customtkinter as ctk

@pytest.fixture
def setup_expense_manager():
    """Fixture for setting up the ExpenseManager instance."""
    em = ExpenseManager()
    em.export_values(1000.0, 800.0, [("Groceries", 150.0), ("Transport", 50.0)])
    em.export_app = ctk.CTk()
    em.export_app.withdraw()  # Minimize the app for testing

    # Simulate the archivename_entry input field
    em.archivename_entry = ctk.CTkEntry(em.export_app)
    em.archivename_entry.insert(0, "TestExportFile")
    return em


# Test 1: Currency Formatting
def test_currency_format():
    result = Functions.currency_format(1250.50)
    assert result == "$1,250.50", "Currency formatting failed for float input."

    result = Functions.currency_format(1000.50)
    assert result == "$1,000.50", "Currency formatting failed for another float input."


# Test 2: Raw Currency Conversion
def test_currency_raw():
    result = Functions.currency_raw("1,250.50")
    assert result == 1250.5, "Currency raw conversion failed for valid string input."

    result = Functions.currency_raw("1,000.50")
    assert result == 1000.5, "Currency raw conversion failed for another valid string input."



# Test 3: Expense Export Validation
def test_export_pdf(setup_expense_manager,tmpdir):
    # Step 1: Mock the file name entry field
    export_dir = tmpdir.mkdir("export")
    
    # Step 2: Simulate selecting a folder by overriding askdirectory
    def fake_askdirectory(title):
        return str(export_dir)

    ctk.filedialog.askdirectory = fake_askdirectory

    # Step 3: Call the export_pdf1 method
    setup_expense_manager.export_pdf1()

    # Step 4: Check if the file was created
    exported_file = os.path.join(str(export_dir), "TestExportFile.pdf")
    assert os.path.exists(exported_file), "Exported PDF file does not exist."


# Test 4: Expense Addition Updates Balance
def test_update_balance(setup_expense_manager):
    initial_balance = setup_expense_manager.current_balance
    setup_expense_manager.expenses.append(("Dining", 100.0))
    setup_expense_manager.current_balance -= 100.0
    assert setup_expense_manager.current_balance == initial_balance - 100.0, \
        "Balance update after adding expense failed."


# Test 5: Import Expense Values
def test_import_values(setup_expense_manager, tmpdir):
    tmp_file = tmpdir.join("mock_file.xlsx")
    mock_data = pd.DataFrame({
        "Balance": ["1000"],
        "Expense": ["Rent"],
        "Expense Amount": ["800"],
    })
    mock_data.to_excel(tmp_file, index=False, engine='openpyxl')

    # Step 2: Override the file dialog to return the path of the temporary file
    def fake_askopenfilename():
        return str(tmp_file)

    setup_expense_manager.currency_raw = lambda x: float(x)  # Simplify raw currency parsing for testing
    setup_expense_manager.import_values = lambda: setup_expense_manager.import_values_impl(fake_askopenfilename)

    # Step 3: Implement a wrapper for the original import_values logic
   




