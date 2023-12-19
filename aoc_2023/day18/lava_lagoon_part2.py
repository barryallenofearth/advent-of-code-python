import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([UDLR])\s+(\d+)\s+\((#[a-f\d]+)\)")


def get_min_max(corners: list[Coordinates]) -> tuple[Coordinates, Coordinates]:
    x_min = 1
    x_max = 1
    y_min = 1
    y_max = 1
    for corner in corners:
        if corner.x < x_min:
            x_min = corner.x
        if corner.x > x_max:
            x_max = corner.x
        if corner.y < y_min:
            y_min = corner.y
        if corner.y > y_max:
            y_max = corner.y

    return Coordinates(x_min, y_min), Coordinates(y_max, y_max)


def find_inside_corners(corners: list[Coordinates], horizontal_lines: list[tuple[Coordinates, Coordinates]]) -> list[Coordinates]:
    min_coordinates, max_coordinates = get_min_max(corners)

    # find top horizontal line and most lost position
    top_lines = list(filter(lambda line: line[0].y == min_coordinates.y, horizontal_lines))
    top_lines.sort(key=lambda line: line[0].x if line[0].x < line[1].x else line[1].x)

    # if first position in the line tuple is larger than the second, the direction of corners is backwards => reverse
    first_position = top_lines[0][0]
    second_position = top_lines[0][1]
    top_line_start_index = corners.index(first_position)
    if first_position.x > second_position.x:
        corners = corners[::-1]
        top_line_start_index = corners.index(second_position)

    inside_corners = set()
    outside_corners = set()
    for index in range(len(corners)):
        corner = corners[(top_line_start_index + index) % len(corners)]
        next_corner = corners[(top_line_start_index + index + 1) % len(corners)]
        second_next_corner = corners[(top_line_start_index + index + 2) % len(corners)]
        # corner turning left are inside
        # first line up and second left
        print(corner, next_corner, second_next_corner)
        if (corner.x == next_corner.x and corner.y > next_corner.y) and (second_next_corner.x < next_corner.x):
            print(f"add {next_corner}")
            inside_corners.add(next_corner)
        # first line horizontal to the left and second down
        elif (corner.y == next_corner.y and corner.x > next_corner.x) and second_next_corner.y > next_corner.y:
            print(f"add {next_corner}")
            inside_corners.add(next_corner)
        # first line horizontal to the right and second up
        elif (corner.y == next_corner.y and corner.x < next_corner.x) and second_next_corner.y < next_corner.y:
            print(f"add {next_corner}")
            inside_corners.add(next_corner)
        # first line down and second right
        elif (corner.x == next_corner.x and corner.y < next_corner.y) and (second_next_corner.x > next_corner.x):
            print(f"add {next_corner}")
            inside_corners.add(next_corner)
        else:
            outside_corners.add(next_corner)

    print(inside_corners)
    print(len(outside_corners), len(inside_corners), len(outside_corners) + len(inside_corners) - (len(corners) - 1))
    print("found all corners" if len(outside_corners) - len(inside_corners) == 4 else "did not find all corners")


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

vertical_lines = [(corners[index - 1], corners[index]) for index in range(1, len(corners)) if corners[index - 1].x - corners[index].x == 0]
horizontal_lines = [(corners[index - 1], corners[index]) for index in range(1, len(corners)) if corners[index - 1].x - corners[index].x != 0]

print(vertical_lines)
print(horizontal_lines)
inside_corners = find_inside_corners(corners, horizontal_lines)

inside_count = 0
print(f"The total number of pool tiles is {len(facing_grid) + inside_count}.")
