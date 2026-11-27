from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ExpenseChart(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def show_pie_chart(self, data):
        """
        data = [
            ("Food", 120),
            ("Travel", 80),
            ("Shopping", 60)
        ]
        """

        self.figure.clear()

        axis = self.figure.add_subplot(111)

        if not data:
            axis.text(
                0.5,
                0.5,
                "No Expense Data",
                ha="center",
                va="center",
                fontsize=14
            )

            self.canvas.draw()
            return

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        axis.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        axis.set_title("Expense by Category")
        axis.axis("equal")

        self.canvas.draw()

    def show_monthly_chart(self, data):
        """
        data = [
            ("2026-01",120),
            ("2026-02",180)
        ]
        """

        self.figure.clear()

        axis = self.figure.add_subplot(111)

        if not data:
            axis.text(
                0.5,
                0.5,
                "No Monthly Data",
                ha="center",
                va="center",
                fontsize=14
            )

            self.canvas.draw()
            return

        months = [row[0] for row in data]
        totals = [row[1] for row in data]

        axis.bar(months, totals)

        axis.set_title("Monthly Expenses")
        axis.set_xlabel("Month")
        axis.set_ylabel("Amount")

        axis.tick_params(axis="x", rotation=45)

        self.figure.tight_layout()

        self.canvas.draw()