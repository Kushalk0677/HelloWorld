import tkinter as tk
from tkinter import ttk
from random import sample


class Sudoku:
    def __init__(self):
        self.grid = [[0] * 9 for _ in range(9)]
        self.generate_puzzle()

    def generate_puzzle(self):
        base = 3
        side = base * base

        # pattern for a baseline valid solution
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s):
            return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        for r in rows:
            for c in cols:
                self.grid[r][c] = nums[pattern(r, c)]

        # remove some digits to create the puzzle
        for p in sample(range(side * side), 40):
            self.grid[p // side][p % side] = 0

    def is_valid(self, row, col, num):
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True
        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def get_grid(self):
        return self.grid


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.sudoku = Sudoku()
        self.create_widgets()

    def create_widgets(self):
        self.entry_widgets = []
        for i in range(9):
            row_widgets = []
            for j in range(9):
                entry = ttk.Entry(self.root, width=3)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, str(self.sudoku.get_grid()[i][j]))
                row_widgets.append(entry)
            self.entry_widgets.append(row_widgets)

        solve_button = ttk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, columnspan=9, pady=5)

    def solve_sudoku(self):
        for i in range(9):
            for j in range(9):
                value = self.entry_widgets[i][j].get()
                if value:
                    self.sudoku.get_grid()[i][j] = int(value)
        if self.sudoku.solve():
            for i in range(9):
                for j in range(9):
                    self.entry_widgets[i][j].delete(0, tk.END)
                    self.entry_widgets[i][j].insert(0, str(self.sudoku.get_grid()[i][j]))
        else:
            print("No solution exists for the given puzzle.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
