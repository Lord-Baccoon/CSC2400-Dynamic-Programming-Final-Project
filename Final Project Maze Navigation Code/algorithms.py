import random
from collections import deque
from display import display_maze

POPULATION_SIZE = 100
MAX_GENERATIONS = 500
MUTATION_RATE = 0.05
ELITE_COUNT = 5

#checks surroundings
def get_neighbors(maze, position):
    row, col = position

    directions = [
        (0, 1),   # Right
        (1, 0),   # Down
        (0, -1),  # Left
        (-1, 0)   # Up
    ]

    neighbors = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if (0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[new_row])):

            if maze[new_row][new_col] != "#":
                neighbors.append((new_row, new_col))

    return neighbors


#reconstruct the final path
def reconstruct_path(parent, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path


#BFS
def bfs(maze, start, end, animate=False):

    queue = deque([start])
    discovered = {start}
    visited = set()
    parent = {start: None}

    peak_frontier = 1

    while queue:

        current = queue.popleft()
        visited.add(current)

        if animate:
            display_maze(
                maze, visited, current,
                title="BREADTH-FIRST SEARCH"
            )

        if current == end:

            return (
                reconstruct_path(parent, end),
                visited,
                len(discovered),
                peak_frontier
            )

        for neighbor in get_neighbors(maze, current):

            if neighbor not in discovered:

                discovered.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

        peak_frontier = max(peak_frontier, len(queue))

    return [], visited, len(discovered), peak_frontier


#DFS
def dfs(maze, start, end, animate=False):

    stack = [start]
    discovered = {start}
    visited = set()
    parent = {start: None}

    peak_frontier = 1

    while stack:

        current = stack.pop()
        visited.add(current)

        if animate:
            display_maze(
                maze, visited, current,
                title="DEPTH-FIRST SEARCH"
            )

        if current == end:

            return (
                reconstruct_path(parent, end),
                visited,
                len(discovered),
                peak_frontier
            )

        for neighbor in reversed(get_neighbors(maze, current)):

            if neighbor not in discovered:

                discovered.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

        peak_frontier = max(peak_frontier, len(stack))

    return [], visited, len(discovered), peak_frontier


#distance from current position and end point
def heuristic(position, end):
    return (
        abs(position[0] - end[0])
        + abs(position[1] - end[1])
    )


def calculate_fitness(path, end):

    if path[-1] == end:

        return 10000 - len(path)

    distance = heuristic(path[-1], end)

    return -distance * 10


def generate_random_path(maze, start, end, prefix=None):

    path = prefix.copy() if prefix else [start]

    visited = set(path)

    while path[-1] != end:

        current = path[-1]

        neighbors = [
            neighbor
            for neighbor in get_neighbors(maze, current)
            if neighbor not in visited
        ]

        #stop if we reach a dead end
        if not neighbors:
            break

        next_position = random.choice(neighbors)

        path.append(next_position)
        visited.add(next_position)

    return path


def crossover(parent1, parent2):

    common_nodes = list(
        set(parent1[1:]) & set(parent2[1:])
    )

    if not common_nodes:
        return parent1.copy()

    crossover_point = random.choice(common_nodes)

    index1 = parent1.index(crossover_point)
    index2 = parent2.index(crossover_point)

    child = (
        parent1[:index1]
        + parent2[index2:]
    )

    #no loops
    if len(child) != len(set(child)):
        return parent1.copy()

    return child

def mutate(maze, start, end, path):

    if random.random() >= MUTATION_RATE:
        return path

    mutation_point = random.randint(0, len(path) - 1)

    prefix = path[:mutation_point + 1]

    return generate_random_path(
        maze, start, end, prefix
    )


def genetic_algorithm(maze, start, end, animate=False):

    population = [
        generate_random_path(maze, start, end)
        for _ in range(POPULATION_SIZE)
    ]

    explored = set()

    peak_frontier = len(population)

    for generation in range(MAX_GENERATIONS):

        #record all positions reached
        for path in population:

            explored.update(path)

        population.sort(
            key=lambda path: calculate_fitness(path, end),
            reverse=True
        )

        best_path = population[0]

        if animate:
            display_maze(
                maze,
                explored,
                path=best_path,
                title=f"GENETIC ALGORITHM | Generation {generation + 1}"
            )

        #check if the best reached the end
        if best_path[-1] == end:

            return (
                best_path,
                explored,
                len(explored),
                peak_frontier
            )

        #save the best individuals
        new_population = [
            path.copy()
            for path in population[:ELITE_COUNT]
        ]

        #select parents from the top half
        parent_pool = population[:POPULATION_SIZE // 2]

        while len(new_population) < POPULATION_SIZE:

            parent1 = random.choice(parent_pool)
            parent2 = random.choice(parent_pool)

            child = crossover(parent1, parent2)

            child = mutate(
                maze, start, end, child
            )

            new_population.append(child)

        population = new_population

        peak_frontier = max(
            peak_frontier,
            len(population)
        )

    #no sol
    return [], explored, len(explored), peak_frontier