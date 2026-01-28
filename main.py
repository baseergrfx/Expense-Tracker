import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import date

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        
        # Database connection
        self.db = Database()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

        # Variables
        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.description_var = tk.StringVar()
        
        self.create_widgets()
        self.refresh_expenses()

    def create_widgets(self):
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self.root, text="Add New Expense", padding=(20, 10))
        input_frame.pack(fill="x", padx=20, pady=10)

        # Date
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.date_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Category
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        categories = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
        ttk.Combobox(input_frame, textvariable=self.category_var, values=categories).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.amount_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Description
        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.description_var).grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Add Button
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # --- List Frame ---
        list_frame = ttk.LabelFrame(self.root, text="Expense History", padding=(20, 10))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview
        columns = ("ID", "Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Category", width=150)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=300)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind delete
        self.tree.bind("<Delete>", self.delete_expense)
        
        # --- Summary Frame ---
        summary_frame = ttk.Frame(self.root, padding=(20, 10))
        summary_frame.pack(fill="x", padx=20, pady=5)
        
        self.total_label = ttk.Label(summary_frame, text="Total Expenses: $0.00", font=("Helvetica", 14, "bold"))
        self.total_label.pack(side="right")

    def add_expense(self):
        try:
            date_val = self.date_var.get()
            cat_val = self.category_var.get()
            amount_val = self.amount_var.get()
            desc_val = self.description_var.get()

            if not date_val or not cat_val or amount_val <= 0:
                messagebox.showerror("Error", "Please fill valid Date, Category and Amount > 0")
                return

            self.db.add_expense(date_val, cat_val, amount_val, desc_val)
            self.refresh_expenses()
            self.clear_inputs()
            messagebox.showinfo("Success", "Expense Added!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {e}")

    def refresh_expenses(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get data
        expenses = self.db.get_expenses()
        total = 0.0
        
        for exp in expenses:
            self.tree.insert("", "end", values=exp)
            total += exp[3] # Amount index
            
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

    def clear_inputs(self):
        self.category_var.set("")
        self.amount_var.set(0.0)
        self.description_var.set("")
        # Keep date as today

    def delete_expense(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        item = self.tree.item(selected_item)
        expense_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            self.db.delete_expense(expense_id)
            self.refresh_expenses()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
