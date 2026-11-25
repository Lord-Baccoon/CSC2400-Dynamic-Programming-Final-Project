import time

DELAY = 0.01

#ANSI color codes
RESET = "\033[0m"
GRAY = "\033[90m"
WHITE = "\033[97m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BLUE = "\033[94m"


def display_maze(maze, visited=None, current=None,
                 path=None, title=None):

    visited = visited or set()
    path = set(path or [])

    separator = "━" * (len(maze[0]) + 10)

    print("\n\n")
    print(WHITE + separator + RESET)

    if title:
        print(CYAN + title + RESET)
        print(WHITE + separator + RESET)

    for row in range(len(maze)):

        line = ""

        for col in range(len(maze[row])):

            position = (row, col)
            cell = maze[row][col]

            if cell == "S":
                line += CYAN + "S" + RESET

            elif cell == "E":
                line += RED + "E" + RESET

            elif cell == "#":
                line += GRAY + "█" + RESET

            elif position == current:
                line += YELLOW + "◆" + RESET

            elif position in path:
                line += GREEN + "█" + RESET

            elif position in visited:
                line += BLUE + "·" + RESET

            else:
                line += " "

        print(line)

    print(WHITE + separator + RESET)

    time.sleep(DELAY)