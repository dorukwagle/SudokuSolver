from tkinter import ttk
import tkinter as tk

total_rows = 9
total_cols = 9


def print_puzzle(puzzle):
    for row in puzzle:
        print(*[value if value else 0 for value in row])


# check whether the given number is allowed in the given row/column
def check_number(puzzle, row, column, number):
    # if the number is 0 do not check it
    if not number:
        return True
    # check if number exists in row
    row_t = puzzle[row]
    for ind, num in enumerate(row_t):
        if ind == column:
            continue
        if num == number:
            return False
    # check if the number exists in the column
    col = [row[column] for row in puzzle]
    for ind, num in enumerate(col):
        # since the column is converted into row
        if ind == row:
            continue
        if num == number:
            return False
    # since the number is allowed the given position
    return True


def validate_puzzle(puzzle):
    for i in range(total_rows):
        for j in range(total_cols):
            # now check if the number in each cell is allowed
            if not check_number(puzzle, i, j, puzzle[i][j]):
                return False
    return True


class Puzzle(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # create a list to hold reference to all combobox
        self.refer_holder = []
        self.numbers_holder = []
        base_frame = ttk.Frame(self)
        base_frame.pack()

        puzzle_frame = ttk.Frame(base_frame)
        # puzzle_frame.grid_propagate(False)
        puzzle_frame.pack(side="left")

        # create the number boxes
        for row in range(total_rows):
            self.refer_holder.append([])
            for col in range(total_cols):
                cell = ttk.Combobox(puzzle_frame, values=list(range(1, 10)), state="readonly", takefocus=0,
                                    width=3, font=("", 20))
                cell.grid(row=row, column=col)
                self.refer_holder[-1].append(cell)

        # add a button to confirm the puzzle
        btn = ttk.Button(base_frame, text="Confirm Puzzle")
        btn.bind("<ButtonRelease>", self.confirm)
        btn.pack(side="right", fill="x", expand=True, ipadx=20, ipady=20)

    def confirm(self, _):
        # reset the number holder
        self.numbers_holder.clear()
        for row in self.refer_holder:
            self.numbers_holder.append([])
            for col in row:
                self.numbers_holder[-1].append(col.get())
        if validate_puzzle(self.numbers_holder):
            print_puzzle(self.numbers_holder)
        else:
            print("invalid puzzle")


tk = tk.Tk()
Puzzle(tk).pack()
tk.mainloop()
