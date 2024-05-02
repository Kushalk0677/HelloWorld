import datetime
import json
import tkinter as tk
from tkinter import messagebox

class FinancialManagementTool:
    def __init__(self):
        self.budget = {}
        self.expenses = []
        self.investment_portfolio = []

    def load_data(self):
        # Load existing data from files or database
        # Example: Load budget, expenses, and investment portfolio from JSON files
        try:
            with open('budget.json', 'r') as file:
                self.budget = json.load(file)
        except FileNotFoundError:
            pass
        try:
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            pass
        try:
            with open('investment_portfolio.json', 'r') as file:
                self.investment_portfolio = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        # Save data to files or database
        with open('budget.json', 'w') as file:
            json.dump(self.budget, file, indent=4)
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file, indent=4)
        with open('investment_portfolio.json', 'w') as file:
            json.dump(self.investment_portfolio, file, indent=4)

    def add_expense(self, category, amount, description):
        # Add a new expense
        expense = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'category': category,
            'amount': amount,
            'description': description
        }
        self.expenses.append(expense)
        self.save_data()

    def add_income(self, category, amount, description):
        # Add income to budget
        if category in self.budget:
            self.budget[category] += amount
        else:
            self.budget[category] = amount
        self.save_data()

    def add_investment(self, investment):
        # Add a new investment to the portfolio
        self.investment_portfolio.append(investment)
        self.save_data()

    def view_budget(self):
        # View current budget
        messagebox.showinfo("Budget", self.budget)

    def view_expenses(self):
        # View expenses
        messagebox.showinfo("Expenses", self.expenses)

    def view_investment_portfolio(self):
        # View investment portfolio
        messagebox.showinfo("Investment Portfolio", self.investment_portfolio)

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Management Tool")

        self.tool = FinancialManagementTool()
        self.tool.load_data()

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.add_expense_btn = tk.Button(self.menu_frame, text="Add Expense", command=self.add_expense)
        self.add_expense_btn.grid(row=0, column=0, padx=5)

        self.add_income_btn = tk.Button(self.menu_frame, text="Add Income", command=self.add_income)
        self.add_income_btn.grid(row=0, column=1, padx=5)

        self.add_investment_btn = tk.Button(self.menu_frame, text="Add Investment", command=self.add_investment)
        self.add_investment_btn.grid(row=0, column=2, padx=5)

        self.view_budget_btn = tk.Button(self.menu_frame, text="View Budget", command=self.view_budget)
        self.view_budget_btn.grid(row=1, column=0, columnspan=3, pady=5, sticky="WE")

        self.view_expenses_btn = tk.Button(self.menu_frame, text="View Expenses", command=self.view_expenses)
        self.view_expenses_btn.grid(row=2, column=0, columnspan=3, pady=5, sticky="WE")

        self.view_investment_portfolio_btn = tk.Button(self.menu_frame, text="View Investment Portfolio", command=self.view_investment_portfolio)
        self.view_investment_portfolio_btn.grid(row=3, column=0, columnspan=3, pady=5, sticky="WE")

    def add_expense(self):
        expense_window = tk.Toplevel(self.root)
        expense_window.title("Add Expense")

        category_label = tk.Label(expense_window, text="Category:")
        category_label.grid(row=0, column=0, padx=5, pady=5)

        category_entry = tk.Entry(expense_window)
        category_entry.grid(row=0, column=1, padx=5, pady=5)

        amount_label = tk.Label(expense_window, text="Amount:")
        amount_label.grid(row=1, column=0, padx=5, pady=5)

        amount_entry = tk.Entry(expense_window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)

        description_label = tk.Label(expense_window, text="Description:")
        description_label.grid(row=2, column=0, padx=5, pady=5)

        description_entry = tk.Entry(expense_window)
        description_entry.grid(row=2, column=1, padx=5, pady=5)

        submit_btn = tk.Button(expense_window, text="Submit", command=lambda: self.tool.add_expense(category_entry.get(), float(amount_entry.get()), description_entry.get()))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def add_income(self):
        income_window = tk.Toplevel(self.root)
        income_window.title("Add Income")

        category_label = tk.Label(income_window, text="Category:")
        category_label.grid(row=0, column=0, padx=5, pady=5)

        category_entry = tk.Entry(income_window)
        category_entry.grid(row=0, column=1, padx=5, pady=5)

        amount_label = tk.Label(income_window, text="Amount:")
        amount_label.grid(row=1, column=0, padx=5, pady=5)

        amount_entry = tk.Entry(income_window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)

        description_label = tk.Label(income_window, text="Description:")
        description_label.grid(row=2, column=0, padx=5, pady=5)

        description_entry = tk.Entry(income_window)
        description_entry.grid(row=2, column=1, padx=5, pady=5)

        submit_btn = tk.Button(income_window, text="Submit", command=lambda: self.tool.add_income(category_entry.get(), float(amount_entry.get()), description_entry.get()))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def add_investment(self):
        investment_window = tk.Toplevel(self.root)
        investment_window.title("Add Investment")

        name_label = tk.Label(investment_window, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tk.Entry(investment_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        amount_label = tk.Label(investment_window, text="Amount:")
        amount_label.grid(row=1, column=0, padx=5, pady=5)

        amount_entry = tk.Entry(investment_window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)

        return_rate_label = tk.Label(investment_window, text="Return Rate (decimal):")
        return_rate_label.grid(row=2, column=0, padx=5, pady=5)

        return_rate_entry = tk.Entry(investment_window)
        return_rate_entry.grid(row=2, column=1, padx=5, pady=5)

        submit_btn = tk.Button(investment_window, text="Submit", command=lambda: self.tool.add_investment({'name': name_entry.get(), 'amount': float(amount_entry.get()), 'return_rate': float(return_rate_entry.get())}))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def view_budget(self):
        self.tool.view_budget()

    def view_expenses(self):
        self.tool.view_expenses()

    def view_investment_portfolio(self):
        self.tool.view_investment_portfolio()

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
