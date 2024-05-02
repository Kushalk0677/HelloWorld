import tkinter as tk
from tkinter import ttk
from algorithmic_trader import main

# List of stocks to choose from
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'NVDA', 'NFLX', 'DIS', 'INTC']

# Function to execute algorithmic trading logic
def execute_algorithmic_trading():
    # Get the selected stock symbol from the dropdown menu
    selected_stock = stock_combobox.get()

    # Call the main function from algorithmic_trader.py and capture the output
    output = main(selected_stock)

    # Display the output in the text widget
    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, str(output))  # Insert the output as a string into the text widget

# Create the main application window
root = tk.Tk()
root.title("Algorithmic Trader GUI")

# Create and configure the main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add a label to display instructions
instructions_label = ttk.Label(main_frame, text="Select a stock and click the button to execute algorithmic trading:")
instructions_label.grid(row=0, column=0, padx=10, pady=10)

# Add a dropdown menu to select the stock
stock_combobox = ttk.Combobox(main_frame, values=stocks)
stock_combobox.grid(row=1, column=0, padx=10, pady=10)
stock_combobox.current(0)  # Set default selection

# Add a button to execute algorithmic trading
execute_button = ttk.Button(main_frame, text="Execute Algorithmic Trading", command=execute_algorithmic_trading)
execute_button.grid(row=2, column=0, padx=10, pady=10)

# Add a text widget to display output
output_text = tk.Text(main_frame, height=10, width=50)
output_text.grid(row=3, column=0, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
