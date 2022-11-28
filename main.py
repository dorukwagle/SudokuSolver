from tkinter import ttk
from tkinter import Button, Tk

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


def defocus(c):
    current = c.get()
    c.set("")
    c.set(current)


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
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: defocus(c))
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
        self.numbers_holder = []
        base_frame = ttk.Frame(self)
        base_frame.pack()
        self.puzzle = puzzle

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
                cell.bind("<<ComboboxSelected>>", lambda e, c=cell: defocus(c))
        # now add control buttons
        Button(control_frame, text="Reset All", font=("", 15, "bold", "italic"), command=self.reset_all) \
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Solve From Here", font=("", 15, "bold", "italic"))\
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        Button(control_frame, text="Solve From Start", font=("", 15, "bold", "italic"))\
            .pack(fill="x", expand=True)
        ttk.Label(control_frame, font=("", 10)).pack()
        self.message = ttk.Label(control_frame, text="", font=("", 15, "bold", "italic"), foreground="green")
        self.message.pack(fill="x", expand=True)

    def reset_all(self, *_):
        for row in self.refer_holder:
            for cell in row:
                if str(cell["state"]) != "disabled":
                    cell.set("")


tk = Tk()
Puzzle(tk).pack()
tk.mainloop()
