import multiprocessing
from functools import partial

from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates


def process_trailhead(starting_point: Coordinates, grid: dict[Coordinates:str]) -> int:
    facings = [facing.UP, facing.RIGHT, facing.DOWN, facing.LEFT]

    def find_next_steps(current_point: Coordinates, current_value: int, grid: dict[Coordinates:str], min_max_coordinates: (Coordinates, Coordinates)) -> list[Coordinates]:

        neighbors_with_numbers = []

        for direction in facings:
            neighbor = facing.move_forward(current_point, direction)
            if coordinates.is_off_grid(neighbor, min_max_coordinates[0], min_max_coordinates[1]):
                continue

            if int(grid[neighbor]) != current_value + 1:
                continue

            neighbors_with_numbers.append(neighbor)

        return neighbors_with_numbers

    min_max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
    next_steps = set()
    next_steps.add(starting_point)

    for current_value in range(9):
        very_next_steps = set()
        for position in next_steps:
            for next_step in find_next_steps(position, current_value, grid, min_max_coordinates):
                very_next_steps.add(next_step)

        next_steps = very_next_steps

    return len(next_steps)


def main():
    TEST_MODE = False
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    with open(file_name, encoding="utf-8") as riddle_input:
        lines = []
        for line in riddle_input:
            lines.append(line.strip())

        grid = coordinates.read_grid(lines)

        trail_heads = coordinates.find_symbols_in_grid(grid, "0")

        pool = multiprocessing.Pool(32)
        trail_scores = pool.map(partial(process_trailhead, grid=grid), trail_heads)

        print(f"Total trail score: {sum(trail_scores)}")


if __name__ == "__main__":
    main()
