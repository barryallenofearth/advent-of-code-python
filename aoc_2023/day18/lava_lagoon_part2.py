import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([UDLR])\s+(\d+)\s+\((#[a-f\d]+)\)")

facing_grid = {}
color_grid = {}

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
position = Coordinates(1, 1)
corners = [position]
for line in lines:
    match = DIGGING_PATTERN.match(line.strip())
    original_step_count = int(match.group(2))
    color = match.group(3)
    direction = color[-1].replace("0", facing.RIGHT).replace("1", facing.DOWN).replace("2", facing.LEFT).replace("3", facing.UP)
    step_count = int(color[1:-1], 16)

    position = facing.move_forward(position, direction, step_count)
    corners.append(position)

print(corners)
inside_count = 0
print(f"The total number of pool tiles is {len(facing_grid) + inside_count}.")
