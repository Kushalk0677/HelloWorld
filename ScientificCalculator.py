import tkinter as tk
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")

        self.equation = tk.StringVar()
        self.equation.set("")

        self.result_label = tk.Label(root, textvariable=self.equation, font=("Arial", 20), anchor="e", bd=10,
                                     bg="white", padx=20, pady=10)
        self.result_label.grid(row=0, column=0, columnspan=6, sticky="nsew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sin', 1, 4), ('cos', 1, 5),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('tan', 2, 4), ('cot', 2, 5),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('log', 3, 4), ('ln', 3, 5),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('π', 4, 4), ('e', 4, 5),
            ('√', 5, 0), ('x^y', 5, 1), ('C', 5, 2), ('DEL', 5, 3), ('(', 5, 4), (')', 5, 5)
        ]

        for (text, row, column) in buttons:
            button = tk.Button(root, text=text, font=("Arial", 16), padx=20, pady=20,
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column, sticky="nsew")

        root.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        root.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.equation.get()))
                self.equation.set(result)
            except:
                self.equation.set("Error")
        elif char == 'C':
            self.equation.set("")
        elif char == 'DEL':
            self.equation.set(self.equation.get()[:-1])
        elif char == '√':
            try:
                result = math.sqrt(float(self.equation.get()))
                self.equation.set(str(result))
            except:
                self.equation.set("Error")
        elif char == 'x^y':
            self.equation.set(self.equation.get() + '**')
        elif char == 'sin':
            self.equation.set('math.sin(' + self.equation.get() + ')')
        elif char == 'cos':
            self.equation.set('math.cos(' + self.equation.get() + ')')
        elif char == 'tan':
            self.equation.set('math.tan(' + self.equation.get() + ')')
        elif char == 'cot':
            self.equation.set('1 / math.tan(' + self.equation.get() + ')')
        elif char == 'log':
            self.equation.set('math.log10(' + self.equation.get() + ')')
        elif char == 'ln':
            self.equation.set('math.log(' + self.equation.get() + ')')
        elif char == 'π':
            self.equation.set(self.equation.get() + 'math.pi')
        elif char == 'e':
            self.equation.set(self.equation.get() + 'math.e')
        elif char == '(':
            self.equation.set(self.equation.get() + '(')
        elif char == ')':
            self.equation.set(self.equation.get() + ')')
        else:
            self.equation.set(self.equation.get() + char)


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
