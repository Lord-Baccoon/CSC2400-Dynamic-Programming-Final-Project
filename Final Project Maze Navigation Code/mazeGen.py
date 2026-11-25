import random

WIDTH = 51
HEIGHT = 25
LOOP_CHANCE = 0.10


def generate_maze():

    #start with exclusively walls
    maze = [
        ["#" for col in range(WIDTH)]
        for row in range(HEIGHT)
    ]

    start = (1, 1)
    end = (HEIGHT - 2, WIDTH - 2)

    stack = [start]

    maze[1][1] = " "

    directions = [
        (0, 2),    # Right
        (0, -2),   # Left
        (2, 0),    # Down
        (-2, 0)    # Up
    ]

    #dfs to make sure its possible
    while stack:

        row, col = stack[-1]

        neighbors = []

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if 0 < nr < HEIGHT - 1 and 0 < nc < WIDTH - 1:

                if maze[nr][nc] == "#":
                    neighbors.append((nr, nc))

        if neighbors:

            nr, nc = random.choice(neighbors)

            #replace the wall between the two positions
            maze[(row + nr) // 2][(col + nc) // 2] = " "

            #open the new position
            maze[nr][nc] = " "

            stack.append((nr, nc))

        else:
            stack.pop()

    #more randomness with loops and alternative routes
    for row in range(1, HEIGHT - 1):

        for col in range(1, WIDTH - 1):

            if maze[row][col] != "#":
                continue

            horizontal = (
                maze[row][col - 1] == " "
                and maze[row][col + 1] == " "
            )

            vertical = (
                maze[row - 1][col] == " "
                and maze[row + 1][col] == " "
            )

            if horizontal or vertical:

                if random.random() < LOOP_CHANCE:
                    maze[row][col] = " "

    #starting and ending positions
    maze[start[0]][start[1]] = "S"
    maze[end[0]][end[1]] = "E"

    return maze


