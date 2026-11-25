from mazeGen import generate_maze
from algorithms import bfs, dfs, genetic_algorithm
from display import display_maze

from benchmark import (
    test_algorithms,
    display_results,
    display_total_results,
    automated_benchmark
)


#find a specific character in the maze
def find_position(maze, character):

    for row in range(len(maze)):
        for col in range(len(maze[row])):

            if maze[row][col] == character:
                return (row, col)

    return None


#main program
def main():

    maze = generate_maze()

    algorithms = {
        "BFS": bfs,
        "DFS (Brute Force)": dfs,
        "Genetic": genetic_algorithm
    }

    while True:

        display_maze(maze)

        print("\n========== MAZE SEARCH SIMULATOR ==========")

        print("1. Test Algorithms")
        print("2. Generate New Maze")
        print("3. Average Benchmark Results")
        print("4. Automated Benchmark")
        print("5. Exit")

        choice = input("\nSelection: ")

        if choice == "1":

            start = find_position(maze, "S")
            end = find_position(maze, "E")

            results = test_algorithms(
                maze, start, end, algorithms, animate=True
            )

            print("\nBENCHMARK RESULTS - CURRENT MAZE")

            display_results(results)

            input("\nPress Enter to continue...")

        elif choice == "2":

            maze = generate_maze()

        elif choice == "3":

            display_total_results()

            input("\nPress Enter to continue...")

        elif choice == "4":

            try:

                num_tests = int(
                    input("\nHow many mazes to test? ")
                )

                if num_tests <= 0:

                    print("Enter a number greater than zero.")

                else:

                    automated_benchmark(
                        num_tests, algorithms
                    )

            except ValueError:

                print("Please enter a valid integer.")

            input("\nPress Enter to continue...")

        elif choice == "5":

            break

        else:

            print("Invalid selection.")

            input("Press Enter to continue...")


if __name__ == "__main__":
    main()