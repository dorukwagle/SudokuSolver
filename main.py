import copy
from tkinter import ttk, Button, Tk
from saves import Saves

total_rows = 9
total_cols = 9


# check whether the given number is allowed in the given row/column i.e. cell
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
    for i in range(total_cols):
        # since the column is converted into row
        if i == row:
            continue
        if puzzle[i][column] == number:
            return False
    # check for the repeatation in the nonet
    nonet_x, nonet_y = 3 * (row // 3), 3 * (column // 3)
    for i in range(nonet_x, nonet_x + 3):
        for j in range(nonet_y, nonet_y + 3):
            if i == row and j == column:
                continue
            if puzzle[i][j] == number:
                return False
    # since the number is allowed the given position
    return True


# check if the given puzzle is valid i.e. if the numbers are repeated in the row or column
def validate_puzzle(puzzle):
    for i in range(total_rows):
        for j in range(total_cols):
            # now check if the number in each cell is allowed
            if not check_number(puzzle, i, j, puzzle[i][j]):
                return False
    return True


def is_solved(puzzle, row, col):
    if puzzle[row][col]:
        return True
    return False


# start solving the given puzzle
def solve_puzzle(solution, row=0, col=0):
    # check if the row or column is 8. that means the row, column or puzzle is solved
    if row == 8 and col == 9:
        return True
    if col == 9:
        # a single row is solved, move the control to hte next row
        row += 1
        col = 0
    # iterate over the puzzle and backtract
    for num in range(1, 10):
        # check if the cell already contains a number
        if is_solved(solution, row, col):
            return solve_puzzle(solution, row, col + 1)

        if check_number(solution, row, col, str(num)):
            solution[row][col] = str(num)

            #  now check if the puzzle gets solved using this permutation
            if solve_puzzle(solution, row, col + 1):
                return True
            # now that the puzzle isn't solved using this possibility,
            # reset the value at this cell to backtrack
            solution[row][col] = ''
    return False


# define the color the the nonet in the board
def get_nonet_style(row, col):
    # 1 = r0, c0, = grey | # 3 = r0, c2, = grey | # 5 = r1, c1, = grey | # 7 = r2, c0, = grey | # 9 = r2, c2, = grey
    # 2 = r0, c1, = white | # 4 = r1, c0, = white | # 6 = r1, c2, = white | # 8 = r2, c1, = white
    row = row // 3
    col = col // 3
    if (
            (row == 0 and col == 0) or
            (row == 0 and col == 2) or
            (row == 1 and col == 1) or
            (row == 2 and col == 0) or
            (row == 2 and col == 2)
    ):
        return "dark.TCombobox"
    return "light.TCombobox"


# function that resets all the boxes in the board
def reset_all(references, *_):
    for row in references:
        for cell in row:
            if str(cell["state"]) != "disabled":
                cell.set("")


# called by the class to remove the focus from combobox
def remove_focus(c):
    current = c.get()
    c.set("")
    c.set(current)


# read from the puzzle board
def read_board(board):
    board_data = []
    for row in board:
        board_data.append([])
        for col in row:
            board_data[-1].append(col.get())
    return board_data


# method to display solved puzzle in the number box
def display_in_board(board_reference, solution):
    for i in range(total_rows):
        for j in range(total_cols):
            board_reference[i][j].set(solution[i][j])


class Puzzle(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # create a list to hold reference to all combobox
        self.refer_holder = []
        self.numbers_holder = []
        base_frame = ttk.Frame(self)
        base_frame.pack()
        # initialize database
        self.saves = Saves()

        puzzle_frame = ttk.Frame(base_frame)
        # puzzle_frame.grid_propagate(False)
        puzzle_frame.pack(side="left")

        control_frame = ttk.Frame(base_frame)
        control_frame.pack(side="right")

        # create the number boxes
        for row in range(total_rows):
            self.refer_holder.append([])
            for col in range(total_cols):
                cell = ttk.Combobox(puzzle_frame, values=list(range(1, 10)), state="readonly", takefocus=0,
                                    width=3, font=("", 20, "bold", "italic"), style=get_nonet_style(row, col))
                cell.grid(row=row, column=col)
                cell.bind("<Button>", lambda e: self.err.config(text=""))
                cell.bind("<Button-3>", lambda e, c=cell: c.set("") if str(c["state"]) != "disabled" else None)
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: remove_focus(c))
                self.refer_holder[-1].append(cell)

        ttk.Label(control_frame, text="Fill the Puzzle to Solve", font=("", 13, "bold", "italic")) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, text="", font=("", 15)).pack(fill="x")

        Button(control_frame, text="Reset All", font=("", 15, "bold", "italic"),
               command=lambda: reset_all(self.refer_holder)) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, text="", font=("", 15)).pack(fill="x")

        Button(control_frame, text="Save Puzzle", font=("", 15, "bold", "italic"),
               command=self.save_puzzle) \
            .pack(fill="x")
        ttk.Label(control_frame, text="", font=("", 15)).pack(fill="x")

        saves = ttk.Combobox(control_frame, values=self.saves.get_puzzle_names(),
                             state="readonly", font=("", 12, "bold", "italic"), takefocus=0)
        saves.set("<<Load Saved Puzzles>>")
        saves.pack(fill="x")
        saves.bind("<<ComboboxSelected>>", lambda e, c=saves: self.load_saved_puzzle(c))
        ttk.Label(control_frame, text="", font=("", 15)).pack(fill="x")
        # add a button to confirm the puzzle
        btn = Button(control_frame, text="Confirm Puzzle", font=("", 15, "bold", "italic"))

        btn.bind("<ButtonRelease>", self.confirm)
        btn.pack(side="bottom", fill="x", ipadx=20, ipady=20)

        # display error message
        self.err = ttk.Label(control_frame, text="", font=("", 13, "bold"), foreground="red")
        self.err.pack(fill="x")

    def confirm(self, _):
        # reset the number holder
        self.numbers_holder.clear()
        for row in self.refer_holder:
            self.numbers_holder.append([])
            for col in row:
                self.numbers_holder[-1].append(col.get())
        if not validate_puzzle(self.numbers_holder):
            self.err.config(text="Invalid Puzzle")
            return

        # display new page
        Solver(self.parent, self.numbers_holder).pack()
        self.destroy()

    def load_saved_puzzle(self, combobox):
        puzzle = self.saves.get_puzzle(combobox.get())
        display_in_board(self.refer_holder, puzzle)

    def save_puzzle(self):
        puzzle = read_board(self.refer_holder)
        if validate_puzzle(puzzle):
            self.saves.write(puzzle)
            self.err.config(text="Puzzle Saved", foreground="green")
            return
        self.err.config(text="invalid puzzle", foreground="red")


class Solver(ttk.Frame):
    def __init__(self, parent, puzzle):
        super().__init__(parent)
        # create a list to hold reference to all combobox
        self.refer_holder = []
        base_frame = ttk.Frame(self)
        base_frame.pack()
        self.puzzle = puzzle
        self.parent = parent

        puzzle_frame = ttk.Frame(base_frame)
        # puzzle_frame.grid_propagate(False)
        puzzle_frame.pack(side="left")

        control_frame = ttk.Frame(base_frame)
        control_frame.pack(side="right")

        # create the number boxes and fill the puzzle
        for row in range(total_rows):
            self.refer_holder.append([])
            for col in range(total_cols):
                # check if there is number in the given cell
                text = ""
                if not self.puzzle[row][col]:
                    args = dict(values=list(range(1, 10)), state="readonly", takefocus=0, font=("", 20, "italic"))
                else:
                    args = dict(values=list(range(1, 10)), state="disabled", takefocus=0,
                                font=("", 20, "bold", "italic"), foreground="brown")
                    text = self.puzzle[row][col]
                cell = ttk.Combobox(puzzle_frame, width=3, **args, style=get_nonet_style(row, col))
                cell.grid(row=row, column=col)
                cell.set(text)
                self.refer_holder[-1].append(cell)
                cell.bind("<Button-3>", lambda e, c=cell: c.set("") if str(c["state"]) != "disabled" else None)
                cell.bind("<Button>", lambda e: self.message.config(text=""))
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: remove_focus(c))
        # now add control buttons
        Button(control_frame, text="Reset All", font=("", 15, "bold", "italic"),
               command=lambda: reset_all(self.refer_holder)) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Check Status", font=("", 15, "bold", "italic"), command=self.check_status) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Solve From Here", font=("", 15, "bold", "italic"), command=self.solve_from_here) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Solve From Start", font=("", 15, "bold", "italic"), command=self.solve_from_start) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Back", font=("", 15, "bold", "italic"),
               command=self.goto_home).pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        self.message = ttk.Label(control_frame, text="", font=("", 15, "bold", "italic"), foreground="green")
        self.message.pack(fill="x", expand=True)

    def goto_home(self):
        self.destroy()
        Puzzle(self.parent).pack()

    # reset all the cells to initial state

    # method to solve the puzzle
    def solve_from_start(self):
        solved_puzzle = copy.deepcopy(self.puzzle)
        solved = solve_puzzle(solved_puzzle)
        if not solved:
            self.message.config(text="Solution does not exists", foreground="red")
            return
        display_in_board(self.refer_holder, solved_puzzle)

    # check if the current solution of user is valid and whether it can be solved further
    def check_status(self):
        # read board data first
        data = read_board(self.refer_holder)
        # validate the board first
        if not validate_puzzle(data):
            self.message.config(text="Invalid: value repeated", foreground="red")
            return
        if not solve_puzzle(data):
            self.message.config(text="Cannot be Solved", foreground="red")
            return
        self.message.config(text="Can be Solved", foreground="green")

    # method to solve puzzle continuing from users solution
    def solve_from_here(self):
        half_puzzle = read_board(self.refer_holder)
        solved = solve_puzzle(half_puzzle)
        if not validate_puzzle(half_puzzle):
            self.message.config(text="Invalid: value repeated")
            return
        if not solved:
            self.message.config(text="Unsolvable...!!!", foreground="red")
            return
        display_in_board(self.refer_holder, half_puzzle)


tk = Tk()
# configure theme for the board
style = ttk.Style()
light = "white"
dark = "silver"
style.configure("dark.TCombobox", background=dark)
style.map('dark.TCombobox',
          fieldbackground=[('readonly', dark), ('disabled', dark)],
          selectbackground=[('readonly', dark)],
          background=[('readonly', dark), ('disabled', dark)]
          )
style.configure("light.TCombobox", background=light)
style.map('light.TCombobox',
          fieldbackground=[('readonly', light), ('disabled', light)],
          selectbackground=[('readonly', light)],
          background=[('readonly', light), ('disabled', light)]
          )
Puzzle(tk).pack()
tk.mainloop()
