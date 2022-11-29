import sqlite3 as sql


def convert_to_list(lst):
    new_lst = lst.replace("[", "")\
        .replace("]", "")\
        .replace("''", "0")\
        .replace("'", "")\
        .replace(" ", "")\
        .replace("0", '')
    new_lst = new_lst.split(",")
    puzzle = []
    for i in range(9):
        puzzle.append([])
        for j in range(9):
            puzzle[-1].append(
                new_lst[
                    i * 9 + j
                ]
            )
    return puzzle


class Saves:
    def __init__(self):
        self.__conn = sql.connect("saves.db")
        self.__conn.execute("""create table if not exists puzzles(
                            id integer primary key autoincrement, puzzle text);""")

    def write(self, lst):
        lst = str(lst)
        self.__conn.execute(f"insert into puzzles(puzzle) values(?)", [lst])
        self.__conn.commit()

    def get_puzzle_names(self):
        rows = self.__conn.execute("select id from puzzles;")
        lst = []
        for n in rows:
            lst.append(
                f"Puzzle {n[0]}"
            )
        return lst

    def get_puzzle(self, puzzle_name):
        name = int(puzzle_name.split(" ")[1])
        puzzle = self.__conn.execute(f"select puzzle from puzzles where id={name};")
        lst = None
        for row in puzzle:
            lst = row[0]
        return convert_to_list(lst)
