import tkinter as tk
from tkinter import messagebox
import random

class Juego2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")

        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.high_score = self.load_high_score()

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

        # Display score and high score
        score_label = tk.Label(self.window, text=f"Score: {self.score}", font=("Helvetica", 16), fg="#776e65", bg="#eee4da")
        score_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))

        high_score_label = tk.Label(self.window, text=f"High Score: {self.high_score}", font=("Helvetica", 16), fg="#776e65", bg="#eee4da")
        high_score_label.grid(row=0, column=3, columnspan=4, pady=(10, 5))

        for row in range(4):
            for col in range(4):
                cell_value = self.board[row][col]
                cell_text = str(cell_value) if cell_value != 0 else ""
                cell_color = self.get_tile_color(cell_value)

                label = tk.Label(self.window, text=cell_text, font=("Helvetica", 24, "bold"), width=5, height=2, relief="solid", bg=cell_color, fg="#776e65")
                label.grid(row=row+1, column=col, padx=5, pady=5)

    def get_tile_color(self, value):
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#ffffff")

    def spawn_random(self):
        empty_cells = [(row, col) for row in range(4) for col in range(4) if self.board[row][col] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4
            self.draw_board()

    def move(self, direction):
        original_board = [row[:] for row in self.board]

        # Transpose the board if moving up or down
        if direction in ("up", "down"):
            self.board = [list(row) for row in zip(*self.board)]

        for row in range(4):
            self.board[row] = self.compress(self.board[row], direction)
            self.board[row] = self.merge(self.board[row], direction)
            self.board[row] = self.compress(self.board[row], direction)

        # Transpose the board back after moving
        if direction in ("up", "down"):
            self.board = [list(row) for row in zip(*self.board)]

        if original_board != self.board:
            self.spawn_random()
            self.update_score()
            self.draw_board()
        else:
            if not self.moves_available():
                self.game_over()

    def compress(self, line, direction):
        # Remove zeros and move numbers to the left
        if direction in ("left", "up"):
            return [value for value in line if value != 0] + [0] * line.count(0)
        # Remove zeros and move numbers to the right
        elif direction in ("right", "down"):
            return [0] * line.count(0) + [value for value in line if value != 0]

    def merge(self, line, direction):
        # Merge adjacent identical numbers
        if direction in ("left", "up"):
            for i in range(3):
                if line[i] == line[i + 1]:
                    line[i] *= 2
                    line[i + 1] = 0
                    self.score += line[i]
        elif direction in ("right", "down"):
            for i in range(3, 0, -1):
                if line[i] == line[i - 1]:
                    line[i - 1] *= 2
                    line[i] = 0
                    self.score += line[i - 1]
        return line

    def moves_available(self):
        # Check if there are moves available in all directions
        for direction in ["left", "right", "up", "down"]:
            temp_board = [row[:] for row in self.board]
            for row in range(4):
                temp_board[row] = self.compress(temp_board[row], direction)
                temp_board[row] = self.merge(temp_board[row], direction)
                temp_board[row] = self.compress(temp_board[row], direction)
            if temp_board != self.board:
                return True
        return False

    def game_over(self):
        messagebox.showinfo("Game Over", f"Score: {self.score}\nHigh Score: {self.high_score}")
        self.save_high_score()
        self.window.destroy()

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

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
