import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file="expenses.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the expenses table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def add_expense(self, date, category, amount, description):
        """Add a new expense to the database."""
        self.cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        self.conn.commit()

    def get_expenses(self):
        """Retrieve all expenses from the database."""
        self.cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        return self.cursor.fetchall()

    def delete_expense(self, expense_id):
        """Delete an expense by ID."""
        self.cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.conn.commit()

    def __del__(self):
        """Close the connection when the object is destroyed."""
        self.conn.close()
