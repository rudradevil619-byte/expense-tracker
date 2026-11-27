from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
    QDialog,
    QFormLayout,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QHeaderView
)

from PyQt6.QtCore import Qt, QDate

from database import ExpenseDatabase
from charts import ExpenseChart
from export import export_to_csv


class ExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Expense")
        self.setFixedWidth(350)
        self.setStyleSheet("""
            QDialog {
                background: #f7f7f7;
            }
            QLabel {
                color: #222222;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                background: white;
                color: #111111;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #43A047;
            }
        """)

        layout = QFormLayout(self)

        self.title = QLineEdit()

        self.amount = QDoubleSpinBox()
        self.amount.setMaximum(100000000)
        self.amount.setDecimals(2)

        self.category = QComboBox()
        self.category.addItems([
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Health",
            "Entertainment",
            "Others"
        ])

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.notes = QTextEdit()

        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        buttons = QHBoxLayout()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addRow("Title", self.title)
        layout.addRow("Amount", self.amount)
        layout.addRow("Category", self.category)
        layout.addRow("Date", self.date)
        layout.addRow("Notes", self.notes)
        layout.addRow(buttons)

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)


class ExpenseWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db = ExpenseDatabase()

        self.setWindowTitle("Expense Tracker")
        self.resize(1100, 650)

        self.build_ui()
        self.load_data()


    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        title = QLabel("Expense Tracker")
        title.setObjectName("title")

        main_layout.addWidget(title)

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")

        self.search_btn = QPushButton("Search")

        top.addWidget(self.search)
        top.addWidget(self.search_btn)

        main_layout.addLayout(top)

        cards = QGridLayout()

        self.total_card = QLabel("$0")
        self.month_card = QLabel("$0")
        self.count_card = QLabel("0")

        self.total_card.setObjectName("card")
        self.month_card.setObjectName("card")
        self.count_card.setObjectName("card")

        cards.addWidget(QLabel("Total Expense"),0,0)
        cards.addWidget(self.total_card,1,0)

        cards.addWidget(QLabel("This Month"),0,1)
        cards.addWidget(self.month_card,1,1)

        cards.addWidget(QLabel("Transactions"),0,2)
        cards.addWidget(self.count_card,1,2)

        main_layout.addLayout(cards)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Title",
            "Amount",
            "Category",
            "Date",
            "Notes"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        main_layout.addWidget(self.table)

        buttons = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.pie_btn = QPushButton("Pie Chart")
        self.bar_btn = QPushButton("Monthly Chart")
        self.export_btn = QPushButton("Export CSV")

        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.edit_btn)
        buttons.addWidget(self.delete_btn)
        buttons.addStretch()
        buttons.addWidget(self.pie_btn)
        buttons.addWidget(self.bar_btn)
        buttons.addWidget(self.export_btn)

        main_layout.addLayout(buttons)

        self.search_btn.clicked.connect(self.search_expenses)
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn.clicked.connect(self.delete_expense)
        self.export_btn.clicked.connect(self.export_csv)
        self.pie_btn.clicked.connect(self.show_pie)
        self.bar_btn.clicked.connect(self.show_monthly)

        self.setStyleSheet("""

        QMainWindow{
            background:#202124;
        }

        QLabel{
            color:white;
            font-size:13px;
        }

        #title{
            font-size:24px;
            font-weight:bold;
        }

        #card{
            background:#2d2d2d;
            border-radius:8px;
            padding:14px;
            font-size:22px;
            font-weight:bold;
        }

        QPushButton{
            background:#4CAF50;
            color:white;
            border:none;
            padding:8px 18px;
            border-radius:6px;
        }

        QPushButton:hover{
            background:#43A047;
        }

        QLineEdit{
            padding:8px;
        }

        QTableWidget{
            background:white;
            gridline-color:#dddddd;
        }

        """)

    def load_data(self):
        """Load all expenses into the table."""
        expenses = self.db.get_all_expenses()

        self.table.setRowCount(len(expenses))

        for row_index, expense in enumerate(expenses):
            for column_index, value in enumerate(expense):
                item = QTableWidgetItem(str(value))

                if column_index == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row_index, column_index, item)

        self.update_dashboard()

    def update_dashboard(self):
        """Refresh dashboard cards."""

        total = self.db.get_total_expense()
        monthly = self.db.get_month_total()
        count = self.db.expense_count()

        self.total_card.setText(f"${total:.2f}")
        self.month_card.setText(f"${monthly:.2f}")
        self.count_card.setText(str(count))

    def add_expense(self):
        dialog = ExpenseDialog(self)

        if dialog.exec():
            self.db.add_expense(
                dialog.title.text().strip(),
                dialog.amount.value(),
                dialog.category.currentText(),
                dialog.date.date().toString("yyyy-MM-dd"),
                dialog.notes.toPlainText().strip()
            )

            self.load_data()

    def selected_id(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        return int(self.table.item(row, 0).text())

    def edit_expense(self):

        expense_id = self.selected_id()

        if expense_id is None:
            QMessageBox.information(
                self,
                "Edit Expense",
                "Please select an expense."
            )
            return

        row = self.table.currentRow()

        dialog = ExpenseDialog(self)

        dialog.title.setText(
            self.table.item(row, 1).text()
        )

        dialog.amount.setValue(
            float(self.table.item(row, 2).text())
        )

        category = self.table.item(row, 3).text()

        index = dialog.category.findText(category)

        if index >= 0:
            dialog.category.setCurrentIndex(index)

        dialog.date.setDate(
            QDate.fromString(
                self.table.item(row, 4).text(),
                "yyyy-MM-dd"
            )
        )

        dialog.notes.setPlainText(
            self.table.item(row, 5).text()
        )

        if dialog.exec():
            self.db.update_expense(
                expense_id,
                dialog.title.text().strip(),
                dialog.amount.value(),
                dialog.category.currentText(),
                dialog.date.date().toString("yyyy-MM-dd"),
                dialog.notes.toPlainText().strip()
            )

            self.load_data()

    def delete_expense(self):

        expense_id = self.selected_id()

        if expense_id is None:
            QMessageBox.information(
                self,
                "Delete Expense",
                "Select an expense first."
            )
            return

        answer = QMessageBox.question(
            self,
            "Delete",
            "Delete selected expense?"
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.db.delete_expense(expense_id)

            self.load_data()

    def search_expenses(self):

        keyword = self.search.text().strip()

        if keyword == "":
            self.load_data()
            return

        expenses = self.db.search(keyword)

        self.table.setRowCount(len(expenses))

        for row_index, expense in enumerate(expenses):
            for column_index, value in enumerate(expense):
                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value))
                )

    def show_pie(self):
        """Display category-wise expense pie chart."""

        data = self.db.category_totals()

        self.chart_window = ExpenseChart()
        self.chart_window.setWindowTitle("Category Expense Chart")
        self.chart_window.resize(700, 500)
        self.chart_window.show_pie_chart(data)
        self.chart_window.show()

    def show_monthly(self):
        """Display monthly expense bar chart."""

        data = self.db.monthly_totals()

        self.chart_window = ExpenseChart()
        self.chart_window.setWindowTitle("Monthly Expense Chart")
        self.chart_window.resize(700, 500)
        self.chart_window.show_monthly_chart(data)
        self.chart_window.show()

    def export_csv(self):
        """Export all expenses."""

        expenses = self.db.get_all_expenses()

        export_to_csv(self, expenses)
