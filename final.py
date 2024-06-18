import tkinter as tk
from tkinter import messagebox
from itertools import product
import random
from copy import deepcopy

initial_board = [
    [0, 0, 0, 0, 0, 7, 4, 0, 0],
    [0, 0, 4, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 9, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
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

        tk.Button(self.master, text="Solve with CSP", command=self.solve_sudoku).grid(row=3, column=0, pady=10)
        tk.Button(self.master, text="Solve with Genetic Algorithm", command=self.solve_genetic).grid(row=3, column=1, pady=10)

    def solve_sudoku(self):
        if self.solve_with_csp(initial_board):
            for i in range(9):
                for j in range(9):
                    self.board[i][j].set(initial_board[i][j])
        else:
            messagebox.showinfo("No Solution", "This Sudoku puzzle has no solution.")

    def solve_genetic(self):
        solved_board = self.genetic_algorithm_solve(initial_board)
        if solved_board:
            for i in range(9):
                for j in range(9):
                    self.board[i][j].set(solved_board[i][j])
        else:
            messagebox.showinfo("No Solution", "Genetic algorithm couldn't find a solution.")

    def solve_with_csp(self, board):
        def find_empty_cell(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        return (i, j)
            return None

        def get_domain(board, row, col):
            domain = set(range(1, 10))
            for j in range(9):
                if board[row][j] in domain and j != col:
                    domain.remove(board[row][j])

            for i in range(9):
                if board[i][col] in domain and i != row:
                    domain.remove(board[i][col])

            start_row = row - row % 3
            start_col = col - col % 3
            for i, j in product(range(3), range(3)):
                if board[start_row + i][start_col + j] in domain and (start_row + i != row or start_col + j != col):
                    domain.remove(board[start_row + i][start_col + j])

            return list(domain)

        def is_valid(board, row, col, num):
            for j in range(9):
                if board[row][j] == num and j != col:
                    return False

            for i in range(9):
                if board[i][col] == num and i != row:
                    return False

            start_row = row - row % 3
            start_col = col - col % 3
            for i, j in product(range(3), range(3)):
                if board[start_row + i][start_col + j] == num and (start_row + i != row or start_col + j != col):
                    return False

            return True

        def solve_with_csp_recursive(board):
            empty_cell = find_empty_cell(board)
            if not empty_cell:
                return True

            row, col = empty_cell
            domain = get_domain(board, row, col)

            for value in domain:
                board[row][col] = value
                if is_valid(board, row, col, value):
                    if solve_with_csp_recursive(board):
                        return True
                board[row][col] = 0

            return False

        return solve_with_csp_recursive(board)

    def genetic_algorithm_solve(self, board):
        def generate_random_solution():
            return [[random.randint(1, 9) for _ in range(9)] for _ in range(9)]

        def fitness(solution):
            return sum(1 for i in range(9) for j in range(9) if solution[i][j] == board[i][j])

        def crossover(parent1, parent2):
            crossover_point = random.randint(1, 8)
            child = deepcopy(parent1)
            for i in range(9):
                child[i] = parent1[i] if i < crossover_point else parent2[i]
            return child

        def mutate(solution, mutation_rate):
            for i in range(9):
                for j in range(9):
                    if random.random() < mutation_rate:
                        solution[i][j] = random.randint(1, 9)
            return solution

        population_size = 100
        mutation_rate = 0.1
        max_generations = 1000

        population = [generate_random_solution() for _ in range(population_size)]

        for _ in range(max_generations):
            fitness_scores = [fitness(solution) for solution in population]
            if max(fitness_scores) == 81:
                return population[fitness_scores.index(81)]

            parents = [population[i] for i in sorted(range(population_size), key=lambda k: fitness_scores[k], reverse=True)[:10]]
            new_population = parents[:]

            while len(new_population) < population_size:
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)
                child = mutate(crossover(parent1, parent2), mutation_rate)
                new_population.append(child)

            population = new_population

        return None

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root)

    for i in range(9):
        for j in range(9):
            if initial_board[i][j] != 0:
                game.board[i][j].set(initial_board[i][j])

    root.mainloop()
