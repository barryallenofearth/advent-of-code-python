import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement.coordinates import Coordinates

NORTH = "north"
WEST = "west"
SOUTH = "south"
EAST = "east"


def roll_rocks(grid: dict[Coordinates:str], direction: str, min_coordinates: Coordinates, max_coordinates: Coordinates):
    rolling_stones = coordinates.find_symbols_in_grid(grid, "O")

    if direction == NORTH:
        rolling_stones.sort(key=lambda position: (position.y, position.x))
    elif direction == WEST:
        rolling_stones.sort(key=lambda position: (position.x, position.y))
    elif direction == SOUTH:
        rolling_stones.sort(key=lambda position: (-position.y, position.x))
    elif direction == EAST:
        rolling_stones.sort(key=lambda position: (-position.x, position.y))

    for position in rolling_stones:
        current_position = position
        while True:
            if direction == NORTH and current_position.y == min_coordinates.y:
                break
            elif direction == WEST and current_position.x == min_coordinates.x:
                break
            elif direction == SOUTH and current_position.y == max_coordinates.y:
                break
            elif direction == EAST and current_position.x == max_coordinates.x:
                break

            if direction == NORTH:
                next_position = Coordinates(current_position.x, current_position.y - 1)
            elif direction == WEST:
                next_position = Coordinates(current_position.x - 1, current_position.y)
            elif direction == SOUTH:
                next_position = Coordinates(current_position.x, current_position.y + 1)
            else:
                next_position = Coordinates(current_position.x + 1, current_position.y)

            if grid[next_position] != ".":
                break

            grid[current_position] = "."
            grid[next_position] = "O"

            current_position = next_position


def run_cycle(grid, min_coordinates: Coordinates, max_coordinates: Coordinates):
    roll_rocks(grid, NORTH, min_coordinates, max_coordinates)
    roll_rocks(grid, WEST, min_coordinates, max_coordinates)
    roll_rocks(grid, SOUTH, min_coordinates, max_coordinates)
    roll_rocks(grid, EAST, min_coordinates, max_coordinates)


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

grid = coordinates.read_grid(lines, 1, 1)

min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
number_of_cycles = 1000000000
pattern_to_search = []
initial_number_of_cycles = 100
for cycle in range(number_of_cycles):
    run_cycle(grid, min_coordinates, max_coordinates)
    rolling_stones = coordinates.find_symbols_in_grid(grid, "O")

    if pattern_to_search == rolling_stones:
        break
    if cycle == initial_number_of_cycles:
        pattern_to_search += rolling_stones

cycle_length = cycle - initial_number_of_cycles
print(f"found cycle length of {cycle_length} repetitions.")

remaining_cycles = number_of_cycles - initial_number_of_cycles - cycle_length
print(f"Total remaining {remaining_cycles} cycles.")
number_of_steps_after_last_complete_cycle = remaining_cycles % cycle_length - 1
print(f"Perform remaining {number_of_steps_after_last_complete_cycle} cycles.")
for cycle in range(number_of_steps_after_last_complete_cycle):
    run_cycle(grid, min_coordinates, max_coordinates)

rolling_stones = coordinates.find_symbols_in_grid(grid, "O")
total_load = 0

for position in rolling_stones:
    current_load = max_coordinates.y - position.y + 1
    total_load += current_load

coordinates.print_grid(grid)

print(f"{total_load} is the total north oriented load")
