import random
from time import perf_counter
from mazeGen import generate_maze
from display import display_maze

total_results = {}
total_tests = 0


def test_algorithms(maze, start, end, algorithms, animate=False):

    global total_tests

    current_results = {}

    for name, search_function in algorithms.items():

        random_state = random.getstate()

        #run the timed search without animation
        start_time = perf_counter()

        path, visited, discovered, peak_frontier = (
            search_function(maze, start, end, animate=False)
        )

        end_time = perf_counter()

        #display the animated search separately
        if animate:

            final_random_state = random.getstate()
            random.setstate(random_state)

            animated_path, animated_visited, _, _ = (
                search_function(maze, start, end, animate=True)
            )

            random.setstate(final_random_state)

            display_maze(
                maze,
                animated_visited,
                path=animated_path
            )

            print("\nAlgorithm:", name)
            print("Nodes explored:", len(visited))
            print("Nodes discovered:", discovered)
            print("Peak frontier:", peak_frontier)

            if path:
                print("Path found!")
                print("Path length:", len(path) - 1)
            else:
                print("No path found.")

            print(f"Execution time: {(end_time - start_time) * 1000:.4f} ms")

            input("\nPress Enter to continue...")

        elapsed_time = (end_time - start_time) * 1000

        current_results[name] = {
            "time": elapsed_time,
            "explored": len(visited),
            "discovered": discovered,
            "frontier": peak_frontier,
            "path": len(path) - 1 if path else 0,
            "optimality": 0,
            "success": int(bool(path))
        }

    #BFS guarantees the shortest path
    shortest_path = current_results["BFS"]["path"]

    #calculate path optimality
    for name, stats in current_results.items():

        if stats["success"]:

            if stats["path"] > 0:

                stats["optimality"] = (shortest_path / stats["path"]) * 100

            else:

                stats["optimality"] = 100


        if name not in total_results:

            total_results[name] = {
                "time": 0,
                "explored": 0,
                "discovered": 0,
                "frontier": 0,
                "path": 0,
                "optimality": 0,
                "success": 0
            }

        for stat in stats:

            total_results[name][stat] += stats[stat]

    total_tests += 1

    for stats in current_results.values():

        stats["success"] *= 100

    return current_results


def display_results(results):

    print("-" * 112)

    print(
        f"{'Algorithm':<15}"
        f"{'Time (ms)':>13}"
        f"{'Explored':>12}"
        f"{'Discovered':>13}"
        f"{'Peak Frontier':>16}"
        f"{'Path Length':>13}"
        f"{'Optimality':>15}"
        f"{'Success':>15}"
    )

    print("-" * 112)

    for name, stats in results.items():

        print(
            f"{name:<15}"
            f"{stats['time']:>13.4f}"
            f"{stats['explored']:>12.2f}"
            f"{stats['discovered']:>13.2f}"
            f"{stats['frontier']:>16.2f}"
            f"{stats['path']:>13.2f}"
            f"{stats['optimality']:>14.2f}%"
            f"{stats['success']:>14.2f}%"
        )

    print("-" * 112)


def display_total_results():

    print("\nAVERAGE BENCHMARK RESULTS")
    print("Total Tests:", total_tests)

    if total_tests == 0:

        print("No benchmarks have been completed.")
        return

    average_results = {}

    for name, stats in total_results.items():

        successes = stats["success"]

        average_results[name] = {
            "time": stats["time"] / total_tests,

            "explored": stats["explored"] / total_tests,

            "discovered": stats["discovered"] / total_tests,

            "frontier": stats["frontier"] / total_tests,

            "path": stats["path"] / successes
                    if successes > 0 else 0,

            "optimality": stats["optimality"] / successes
                          if successes > 0 else 0,

            "success": (successes / total_tests) * 100
        }

    display_results(average_results)


def automated_benchmark(num_tests, algorithms):

    print("\nSTARTING AUTOMATED BENCHMARK")
    print("Number of mazes:", num_tests)

    start_time = perf_counter()

    progress_interval = max(1, num_tests // 10)

    for i in range(num_tests):

        maze = generate_maze()

        start = (1, 1)
        end = (len(maze) - 2, len(maze[0]) - 2)

        #test every algorithm on the same maze
        test_algorithms(maze, start, end, algorithms)

        #display progress approximately every 10%
        if (i + 1) % progress_interval == 0 or i + 1 == num_tests:
            percentage = ((i + 1) / num_tests) * 100

            print(
                f"Progress: {i + 1}/{num_tests}"
                f" ({percentage:.1f}%)"
            )

    end_time = perf_counter()

    elapsed_time = end_time - start_time

    print("\nAUTOMATED BENCHMARK COMPLETE")
    print(f"Mazes tested: {num_tests}")
    print(f"Total algorithm runs: {num_tests * len(algorithms)}")
    print(f"Total elapsed time: {elapsed_time:.4f} seconds")

    display_total_results()