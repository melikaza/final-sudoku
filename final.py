import tkinter as tk
from tkinter import messagebox
from itertools import product

#تعریف حالت اولیه سودوکو
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.configure(bg='lightgray')
        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

        self.entries = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.master, bd=2, relief='solid')
                frame.grid(row=i, column=j, padx=2, pady=2)
                for x in range(3):
                    for y in range(3):
                        entry = tk.Entry(frame, width=2, font=('Arial', 18, 'bold'),
                                         textvariable=self.board[3*i+x][3*j+y], justify='center')
                        entry.grid(row=x, column=y, padx=2, pady=2)
                        self.entries.append(entry)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=3, columnspan=3, pady=10)
