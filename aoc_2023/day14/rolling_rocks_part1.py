import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement.coordinates import Coordinates

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

grid = coordinates.read_grid(lines, 1, 1)

rolling_stones = coordinates.find_symbols_in_grid(grid, "O")

rolling_stones.sort(key=lambda position: (position.y, position.x))

for position in rolling_stones:
    current_position = position
    while True:
        if current_position.y == 1:
            break

        next_position = Coordinates(current_position.x, current_position.y - 1)
        if grid[next_position] != ".":
            break

        grid[current_position] = "."
        grid[next_position] = "O"

        current_position = next_position

coordinates.print_grid(grid)

min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)

rolling_stones = coordinates.find_symbols_in_grid(grid, "O")
total_load = 0

for position in rolling_stones:
    current_load = max_coordinates.y - position.y + 1
    total_load += current_load

print(f"{total_load} is the total north oriented load")
