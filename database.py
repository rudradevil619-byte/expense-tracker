import sqlite3
from datetime import datetime


class ExpenseDatabase:
    def __init__(self, db_name="expense.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            notes TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_expense(self, title, amount, category, expense_date, notes):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO expenses
        (title, amount, category, expense_date, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            amount,
            category,
            expense_date,
            notes
        ))

        conn.commit()
        conn.close()

    def get_all_expenses(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return rows

    def update_expense(
            self,
            expense_id,
            title,
            amount,
            category,
            expense_date,
            notes):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE expenses
        SET
            title=?,
            amount=?,
            category=?,
            expense_date=?,
            notes=?
        WHERE id=?
        """, (
            title,
            amount,
            category,
            expense_date,
            notes,
            expense_id
        ))

        conn.commit()
        conn.close()

    def delete_expense(self, expense_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id=?",
            (expense_id,)
        )

        conn.commit()
        conn.close()

    def search(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        WHERE
            title LIKE ?
            OR category LIKE ?
            OR notes LIKE ?
        ORDER BY expense_date DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()

        conn.close()

        return rows

    def get_total_expense(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def get_month_total(self):
        month = datetime.now().strftime("%Y-%m")

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE substr(expense_date,1,7)=?
        """, (month,))

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def category_totals(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def monthly_totals(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            substr(expense_date,1,7),
            SUM(amount)
        FROM expenses
        GROUP BY substr(expense_date,1,7)
        ORDER BY substr(expense_date,1,7)
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def expense_count(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count