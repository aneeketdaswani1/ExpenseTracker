from exporter import export_screen, export_values, import_values


def currency_format(value):
    """
    Formats the value to the Brazilian standard.

    Parameters:
    - value (float or str): Value to be formatted.

    Returns:
    - str: Formatted value.

    Example:
    >>> currency_format(1250.50)
    '1.250,50'

    >>> currency_format(1000.50)
    '1.000,50'
    """
    return '{:_.2f}'.format(value).replace('.', ',').replace('_', '.')


def currency_raw(value):
    """
    Converts the value to the default float format in Python.

    Parameters:
    - value (str): Value to be converted.

    Returns:
    - float: Converted value.

    Example:
    >>> currency_raw('1.250,50')
    1250.5

    >>> currency_raw('1.000,50')
    1000.5
    """
    return float(value.replace('.', '_').replace(',', '.'))


def export(initial_balance, current_balance, expenses):
    """
    Transfers the user to an export screen for exporting files.

    Parameters:
    - initial_balance (float): Initial balance.
    - current_balance (float): Current balance.
    - expenses (list): List of expenses.

    Example:
    >>> export(3000.50, 1500.50, [('Rent', 1500)])
    >>> export_screen()
    - Displays the export screen for exporting files.
    - Exports the values to the export file.
    - Closes the export screen.
    - Returns to the main screen.
    """
    export_values(initial_balance, current_balance, expenses)
    export_screen()


def importer():
    """
    Directs to another function to import values from a previously exported file.

    Returns:
    - initial_balance (float): Initial balance.
    - expenses (list): List of expenses.
    """
    initial_balance, expenses = import_values()
    print(expenses)
    return initial_balance, expenses
