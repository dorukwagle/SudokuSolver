import copy
from tkinter import ttk, Button, Tk

total_rows = 9
total_cols = 9


# method to print the puzzle in the terminal
def print_puzzle(puzzle):
    for row in puzzle:
        print(*[value if value else 0 for value in row])


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


# called by the class to remove the focus from combobox
def remove_focus(c):
    current = c.get()
    c.set("")
    c.set(current)


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


class Puzzle(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # create a list to hold reference to all combobox
        self.refer_holder = []
        self.numbers_holder = []
        base_frame = ttk.Frame(self)
        base_frame.pack()

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
                                    width=3, font=("", 20, "bold", "italic"))
                cell.grid(row=row, column=col)
                cell.bind("<Button>", lambda e: self.err.config(text=""))
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: remove_focus(c))
                self.refer_holder[-1].append(cell)

        ttk.Label(control_frame, text="Fill the Puzzle to Solve", font=("", 13, "bold", "italic")) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, text="", font=("", 15)).pack(fill="x")
        # add a button to confirm the puzzle
        btn = Button(control_frame, text="Confirm Puzzle", font=("", 15, "bold", "italic"))

        btn.bind("<ButtonRelease>", self.confirm)
        btn.pack(fill="x", expand=True, ipadx=20, ipady=20)

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
                args = {}
                text = ""
                if not self.puzzle[row][col]:
                    args = dict(values=list(range(1, 10)), state="readonly", takefocus=0, font=("", 20, "italic"))
                else:
                    args = dict(values=list(range(1, 10)), state="disabled", takefocus=0,
                                font=("", 20, "bold", "italic"), foreground="brown")
                    text = self.puzzle[row][col]
                cell = ttk.Combobox(puzzle_frame, width=3, **args)
                cell.grid(row=row, column=col)
                cell.set(text)
                self.refer_holder[-1].append(cell)
                cell.bind("<Button-3>", lambda e, c=cell: c.set(""))
                cell.bind("<Button>", lambda e: self.message.config(text=""))
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: remove_focus(c))
        # now add control buttons
        Button(control_frame, text="Reset All", font=("", 15, "bold", "italic"), command=self.reset_all) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Check Status", font=("", 15, "bold", "italic"), command=self.check_status) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Solve From Here", font=("", 15, "bold", "italic")) \
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

    def reset_all(self, *_):
        for row in self.refer_holder:
            for cell in row:
                if str(cell["state"]) != "disabled":
                    cell.set("")

    # method to solve the puzzle
    def solve_from_start(self):
        solved_puzzle = copy.deepcopy(self.puzzle)
        solve_puzzle(solved_puzzle)
        if not solved_puzzle:
            self.message.config(text="Solution does not exists")
            return
        self.display_solution(solved_puzzle)

    # check if the current solution of user is valid and whether it can be solved further
    def check_status(self):
        pass

    # method to solve puzzle from the point of users solution
    def solve_from_here(self):
        pass

    # method to display solved puzzle in the number box
    def display_solution(self, solution):
        for i in range(total_rows):
            for j in range(total_cols):
                self.refer_holder[i][j].set(solution[i][j])


tk = Tk()
Puzzle(tk).pack()
tk.mainloop()
