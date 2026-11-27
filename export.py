import csv

from PyQt6.QtWidgets import QFileDialog, QMessageBox


def export_to_csv(parent, expenses):
    """
    Export all expenses to a CSV file.

    expenses format:
    (id, title, amount, category, expense_date, notes)
    """

    if not expenses:
        QMessageBox.information(
            parent,
            "Export",
            "There are no expenses to export."
        )
        return

    file_name, _ = QFileDialog.getSaveFileName(
        parent,
        "Export Expenses",
        "expenses.csv",
        "CSV Files (*.csv)"
    )

    if not file_name:
        return

    try:
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Title",
                "Amount",
                "Category",
                "Date",
                "Notes"
            ])

            writer.writerows(expenses)

        QMessageBox.information(
            parent,
            "Success",
            "Expenses exported successfully."
        )

    except Exception as error:
        QMessageBox.critical(
            parent,
            "Export Failed",
            str(error)
        )