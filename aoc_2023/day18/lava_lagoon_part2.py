import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([UDLR])\s+(\d+)\s+\((#[a-f\d]+)\)")

facing_grid = {}
color_grid = {}

lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)
position = Coordinates(1, 1)
for line in lines:
    match = DIGGING_PATTERN.match(line.strip())
    color = match.group(3)
    direction = color[-1].replace("0", facing.RIGHT).replace("1", facing.DOWN).replace("2", facing.LEFT).replace("3", facing.UP)
    step_count = int(color[1:-1], 16)
    print(step_count, direction)
    if len(facing_grid) == 0:
        facing_grid[position] = direction
        color_grid[position] = color

    if direction == facing.DOWN or direction == facing.UP:
        facing_grid[position] = direction
    for _ in range(step_count):
        position = facing.move_forward(position, direction)
        facing_grid[position] = direction
        color_grid[position] = color

min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(facing_grid)

starting_direction = None
inside_count = 0
print("start search inside.")
print(max_coordinates.x - min_coordinates.x, max_coordinates.y - min_coordinates.y)

for column in range(min_coordinates.y, max_coordinates.y + 1):
    print(f"{column / ((max_coordinates.y - min_coordinates.y) * 100)}% processed.")
    vertical_count = 0
    starting_direction = None
    for row in range(min_coordinates.x, max_coordinates.x + 1):

        position = Coordinates(row, column)
        if position in facing_grid:
            direction = facing_grid[position]
            if direction == facing.UP or direction == facing.DOWN:
                if starting_direction is None:
                    vertical_count += 1
                    starting_direction = direction
                elif starting_direction != direction:
                    vertical_count += 1
                    starting_direction = None
                else:
                    starting_direction = None
        else:
            starting_direction = None
            if vertical_count % 2 == 1:
                inside_count += 1

print(f"The total number of pool tiles is {len(facing_grid) + inside_count}.")
