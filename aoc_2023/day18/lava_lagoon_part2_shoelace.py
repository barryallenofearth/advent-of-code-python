import math
import re
from collections import defaultdict

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([UDLR])\s+(\d+)\s+\((#[a-f\d]+)\)")

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
position = Coordinates(1, 1)
corners = [position]
border_length = 0
for line in lines:
    match = DIGGING_PATTERN.match(line.strip())
    original_step_count = int(match.group(2))
    color = match.group(3)
    direction = color[-1].replace("0", facing.RIGHT).replace("1", facing.DOWN).replace("2", facing.LEFT).replace("3", facing.UP)
    step_count = int(color[1:-1], 16)
    position = facing.move_forward(position, direction, step_count)
    border_length += step_count
    corners.append(position)

inside_area = 0

for index in range(len(corners) - 1):
    positive = corners[index].x * corners[index + 1].y
    inside_area += positive
    negative = corners[index + 1].x * corners[index].y
    inside_area -= negative


inside_area = inside_area / 2 + border_length / 2 + 1
expected_example_value = 952408144115
print(f"The difference to example expected value is {expected_example_value - inside_area} => {(expected_example_value - inside_area) / expected_example_value * 100}%.")
print(f"The total number of pool tiles is {inside_area}.")
