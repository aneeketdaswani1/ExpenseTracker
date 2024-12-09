from exporter import ExpenseManager 


class Functions:
    """
    A class providing utility functions for managing currency formatting,
    exporting, and importing financial data.
    """

    @staticmethod
    
    def currency_format(value):
        """
        Formats the value to dollar format.

        Parameters:
        - value (float or str): Value to be formatted.

        Returns:
        - str: Formatted value in dollar format.

        Example:
        >>> Functions.currency_format(1250.50)
        '$1,250.50'

        >>> Functions.currency_format(1000.50)
        '$1,000.50'
        """
        return f"${value:,.2f}"


    @staticmethod
    def currency_raw(value):
        """
        Converts a dollar-formatted value to a float.

        Parameters:
        - value (str): Value to be converted.

        Returns:
        - float: Converted value.

        Example:
        >>> Functions.currency_raw('$1,250.50')
        1250.5

        >>> Functions.currency_raw('$1,000.50')
        1000.5
        """
        return float(value.replace('$', '').replace(',', ''))

    @staticmethod
    def export(self,initial_balance, current_balance, expenses):
        """
        Transfers the user to an export screen for exporting files.

        Parameters:
        - initial_balance (float): Initial balance.
        - current_balance (float): Current balance.
        - expenses (list): List of expenses.

        Example:
        >>> Functions.export(3000.50, 1500.50, [('Rent', 1500)])
        >>> export_screen()
        - Displays the export screen for exporting files.
        - Exports the values to the export file.
        - Closes the export screen.
        - Returns to the main screen.
        """
        self.export_values(initial_balance, current_balance, expenses)
        self.export_screen()

    @staticmethod
    def importer(self):
        """
        Directs to another function to import values from a previously exported file.

        Returns:
        - initial_balance (float): Initial balance.
        - expenses (list): List of expenses.
        """
        print("Here")
        initial_balance, expenses = self.import_values()
        return initial_balance, expenses
