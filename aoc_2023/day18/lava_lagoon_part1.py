import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([v^><])\s+(\d+)\s+\((#[a-f\d]+)\)")

facing_grid = {}
color_grid = {}

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
position = Coordinates(1, 1)
for line in lines:
    line = (line.strip().replace("U", facing.UP)
            .replace("D", facing.DOWN)
            .replace("L", facing.LEFT)
            .replace("R", facing.RIGHT))
    match = DIGGING_PATTERN.match(line)
    direction = match.group(1)
    step_count = int(match.group(2))
    color = match.group(3)

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

outside = {}
inside = {}
border_positions = list(facing_grid.keys())
starting_direction = None
for column in range(min_coordinates.y, max_coordinates.y + 1):
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
            if vertical_count % 2 == 0:
                outside[position] = "O"
            else:
                inside[position] = "I"

total_grid = {}
total_grid.update(facing_grid)
total_grid.update(outside)
total_grid.update(inside)

coordinates.print_grid(total_grid)

print(f"The total number of pool tiles is {len(facing_grid) + len(inside)}.")
