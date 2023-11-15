import random
import tkinter as tk
from tkinter import messagebox

class Juego2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")
        self.board = [[0] * 4 for _ in range(4)]
        self.spawn_random()
        self.spawn_random()
        self.draw_board()
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<Right>", self.move_right)
        self.window.bind("<Up>", self.move_up)
        self.window.bind("<Down>", self.move_down)
        self.window.mainloop()

    def draw_board(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        for row in range(4):
            for col in range(4):
                cell_value = self.board[row][col]
                cell_text = str(cell_value) if cell_value != 0 else ""
                label = tk.Label(self.window, text=cell_text, font=("Helvetica", 24, "bold"), width=5, height=2, relief="solid", bd=2)
                label.grid(row=row, column=col, padx=5, pady=5)

    def spawn_random(self):
        empty_cells = [(row, col) for row in range(4) for col in range(4) if self.board[row][col] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        original_board = [row[:] for row in self.board]

        if direction == "left":
            self.board = [self.slide(row) for row in self.board]
        elif direction == "right":
            self.board = [self.slide(row[::-1])[::-1] for row in self.board]
        elif direction == "up":
            self.board = [list(row) for row in zip(*self.board)]
            self.board = [self.slide(row) for row in self.board]
            self.board = [list(row) for row in zip(*self.board)]
        elif direction == "down":
            self.board = [list(row) for row in zip(*self.board)]
            self.board = [self.slide(row[::-1])[::-1] for row in self.board]
            self.board = [list(row) for row in zip(*self.board)]

        if original_board != self.board:
            self.spawn_random()
            self.draw_board()

    def slide(self, row):
        row = [value for value in row if value != 0]
        row = self.merge(row)
        row += [0] * (4 - len(row))
        return row

    def merge(self, row):
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        row = [value for value in row if value != 0]
        row += [0] * (4 - len(row))
        return row

    def move_left(self, event):
        self.move("left")

    def move_right(self, event):
        self.move("right")

    def move_up(self, event):
        self.move("up")

    def move_down(self, event):
        self.move("down")

if __name__ == "__main__":
    juego = Juego2048()
