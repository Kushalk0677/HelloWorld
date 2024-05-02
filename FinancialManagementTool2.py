import datetime
import json
import tkinter as tk
from tkinter import messagebox

class FinancialManagementTool:
    def __init__(self):
        self.budget = {}
        self.expenses = []
        self.assets = {'investments': [], 'real_estate': [], 'savings_accounts': []}

    def load_data(self):
        # Load existing data from files or database
        # Example: Load budget, expenses, and assets from JSON files
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
            with open('assets.json', 'r') as file:
                self.assets = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        # Save data to files or database
        with open('budget.json', 'w') as file:
            json.dump(self.budget, file, indent=4)
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file, indent=4)
        with open('assets.json', 'w') as file:
            json.dump(self.assets, file, indent=4)

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

    def add_asset(self, asset_type, asset):
        # Add a new asset to the appropriate category
        if asset_type in self.assets:
            self.assets[asset_type].append(asset)
            self.save_data()
        else:
            print(f"Asset type '{asset_type}' not supported.")

    def view_budget(self):
        # View current budget
        messagebox.showinfo("Budget", self.budget)

    def view_expenses(self):
        # View expenses
        messagebox.showinfo("Expenses", self.expenses)

    def view_assets(self):
        # View all assets
        assets_info = ''
        for category, assets in self.assets.items():
            assets_info += f"{category.capitalize()}:\n"
            for asset in assets:
                assets_info += f"Name: {asset['name']} - Value: {asset['value']}\n"
            assets_info += '\n'
        messagebox.showinfo("Assets", assets_info)

    def get_summary(self):
        # Get summary of budget, expenses, and assets
        summary = {
            'budget': self.budget,
            'expenses': self.expenses,
            'assets': self.assets
        }
        return summary

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

        self.add_asset_btn = tk.Button(self.menu_frame, text="Add Asset", command=self.add_asset)
        self.add_asset_btn.grid(row=0, column=2, padx=5)

        self.view_budget_btn = tk.Button(self.menu_frame, text="View Budget", command=self.view_budget)
        self.view_budget_btn.grid(row=1, column=0, columnspan=3, pady=5, sticky="WE")

        self.view_expenses_btn = tk.Button(self.menu_frame, text="View Expenses", command=self.view_expenses)
        self.view_expenses_btn.grid(row=2, column=0, columnspan=3, pady=5, sticky="WE")

        self.view_assets_btn = tk.Button(self.menu_frame, text="View Assets", command=self.view_assets)
        self.view_assets_btn.grid(row=3, column=0, columnspan=3, pady=5, sticky="WE")

        self.summary_btn = tk.Button(self.menu_frame, text="Summary", command=self.show_summary)
        self.summary_btn.grid(row=4, column=0, columnspan=3, pady=5, sticky="WE")

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

    def add_asset(self):
        asset_window = tk.Toplevel(self.root)
        asset_window.title("Add Asset")

        asset_type_label = tk.Label(asset_window, text="Asset Type:")
        asset_type_label.grid(row=0, column=0, padx=5, pady=5)

        asset_type_entry = tk.Entry(asset_window)
        asset_type_entry.grid(row=0, column=1, padx=5, pady=5)

        name_label = tk.Label(asset_window, text="Name:")
        name_label.grid(row=1, column=0, padx=5, pady=5)

        name_entry = tk.Entry(asset_window)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        value_label = tk.Label(asset_window, text="Value:")
        value_label.grid(row=2, column=0, padx=5, pady=5)

        value_entry = tk.Entry(asset_window)
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        submit_btn = tk.Button(asset_window, text="Submit", command=lambda: self.tool.add_asset(asset_type_entry.get(), {'name': name_entry.get(), 'value': float(value_entry.get())}))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def view_budget(self):
        self.tool.view_budget()

    def view_expenses(self):
        self.tool.view_expenses()

    def view_assets(self):
        self.tool.view_assets()

    def show_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Summary")

        summary_label = tk.Label(summary_window, text="Summary")
        summary_label.pack(pady=10)

        summary_text = tk.Text(summary_window, height=20, width=50)
        summary_text.pack()

        summary = self.tool.get_summary()
        summary_text.insert(tk.END, json.dumps(summary, indent=4))

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
