import sqlite3 as sql


class Saves:
    def __init__(self):
        self.__conn = sql.connect("saves.db")
        self.__conn.execute("""create table if not exists puzzles(
                            id integer primary key autoincrement, puzzle text);""")

    def write(self, lst):

        self.__conn.execute(f"insert into puzzles(puzzle) values(?)", (str(lst),))
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
        return lst



if __name__ == "__main__":
    saves = Saves()
    saves.write(str(['', 4, 6, 3, 5, 66, '', '', 67]))

    print(saves.get_puzzle_names())
    print()
    print(saves.get_puzzle("Puzzle 0"))
