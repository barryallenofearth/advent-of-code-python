import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

DIGGING_PATTERN = re.compile(r"([UDLR])\s+(\d+)\s+\((#[a-f\d]+)\)")


class Rectangle:

    def __init__(self):
        self.bottom_left = None
        self.bottom_right = None
        self.top_right = None
        self.top_left = None

    def __eq__(self, other):
        return (type(other) == Rectangle and
                self.bottom_left == other.bottom_left and
                self.bottom_right == other.bottom_right and
                self.top_right == other.top_right and
                self.top_left == other.top_left)

    def __repr__(self):
        return f"Rectangle: bottom_left {self.bottom_left},bottom_right {self.bottom_right},top_right {self.top_right},top_left {self.top_left},"

    def __hash__(self):
        return hash(self.__repr__())


def sort_tuple(point1: Coordinates, point2: Coordinates) -> tuple[Coordinates, Coordinates]:
    if point1.x + point1.y > point2.x + point2.y:
        return point1, point2
    else:
        return point2, point1


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
        print("reverse corner order")
        corners = corners[::-1]
        top_line_start_index = corners.index(second_position)

    inside_corners = set()
    outside_corners = set()
    for index in range(len(corners)):
        corner = corners[(top_line_start_index + index) % len(corners)]
        next_corner = corners[(top_line_start_index + index + 1) % len(corners)]
        second_next_corner = corners[(top_line_start_index + index + 2) % len(corners)]
        # corner turning left are inside

        # print(corner, next_corner, second_next_corner)
        # first line up and second left
        if (corner.x == next_corner.x and corner.y > next_corner.y) and (second_next_corner.x < next_corner.x):
            # print(f"(up => left) add {next_corner}")
            inside_corners.add(next_corner)
        # first line horizontal to the left and second down
        elif (corner.y == next_corner.y and corner.x > next_corner.x) and second_next_corner.y > next_corner.y:
            # print(f"(left => down) add {next_corner}")
            inside_corners.add(next_corner)
        # first line horizontal to the right and second up
        elif (corner.y == next_corner.y and corner.x < next_corner.x) and second_next_corner.y < next_corner.y:
            # print(f"(right => up) add {next_corner}")
            inside_corners.add(next_corner)
        # first line down and second right
        elif (corner.x == next_corner.x and corner.y < next_corner.y) and (second_next_corner.x > next_corner.x):
            # print(f"(down => right) add {next_corner}")
            inside_corners.add(next_corner)
        # first line up and second right
        elif (corner.x == next_corner.x and corner.y > next_corner.y) and (second_next_corner.x > next_corner.x):
            # print(f"(up => right) outside")
            outside_corners.add(next_corner)
        # first line horizontal to the left and second up
        elif (corner.y == next_corner.y and corner.x > next_corner.x) and second_next_corner.y < next_corner.y:
            # print(f"(left => up) outside")
            outside_corners.add(next_corner)
        # first line horizontal to the right and second down
        elif (corner.y == next_corner.y and corner.x < next_corner.x) and second_next_corner.y > next_corner.y:
            # print(f"(right => down) outside")
            outside_corners.add(next_corner)
        # first line down and second left
        elif (corner.x == next_corner.x and corner.y < next_corner.y) and (second_next_corner.x < next_corner.x):
            # print(f"(down => left) outside")
            outside_corners.add(next_corner)
        else:
            raise ValueError("Corner could not be processed")

    print(inside_corners)
    print(len(outside_corners), len(inside_corners), len(outside_corners) + len(inside_corners) - (len(corners) - 1))
    print("found all corners" if len(outside_corners) - len(inside_corners) == 4 else f"did not find all corners. missing {len(outside_corners) - len(inside_corners) - 4}")

    return list(inside_corners)


def add_inner_corner_to_outer_border_lines(inside_corners: list[Coordinates], outside_horizontal_lines: list[tuple[Coordinates, Coordinates]],
                                           outside_vertical_lines: list[tuple[Coordinates, Coordinates]]) \
        -> tuple[list[tuple[Coordinates, Coordinates]], list[tuple[Coordinates, Coordinates]]]:
    def determine_missing_directions(corner: Coordinates) -> list[str]:
        missing_facings = []
        for line in outside_horizontal_lines:
            if line[0] == corner:
                if line[1].x < corner.x:
                    missing_facings.append(facing.RIGHT)
                else:
                    missing_facings.append(facing.LEFT)
                break
            elif line[1] == corner:
                if line[0].x < corner.x:
                    missing_facings.append(facing.RIGHT)
                else:
                    missing_facings.append(facing.LEFT)
                break
        for line in outside_vertical_lines:
            if line[0] == corner:
                if line[1].y > corner.y:
                    missing_facings.append(facing.UP)
                else:
                    missing_facings.append(facing.DOWN)
                break
            elif line[1] == corner:
                if line[0].y > corner.y:
                    missing_facings.append(facing.UP)
                else:
                    missing_facings.append(facing.DOWN)
                break

        if len(missing_facings) != 2:
            raise ValueError(f"Found {len(missing_facings)} additional facings instead of 2.")
        return missing_facings

    added_horizontal_lines = set()
    added_vertical_lines = set()

    for corner in inside_corners:
        missing_facings = determine_missing_directions(corner)
        for direction in missing_facings:
            if direction == facing.LEFT:
                next_corner_line = sorted(filter(lambda line: line[0].x < corner.x and ((line[0].y <= corner.y <= line[1].y) or (line[1].y <= corner.y <= line[0].y)), outside_vertical_lines),
                                          key=lambda line: abs(line[0].x - corner.x))[0]
                added_horizontal_lines.add(sort_tuple(corner, Coordinates(next_corner_line[0].x, corner.y)))
            elif direction == facing.RIGHT:
                next_corner_line = sorted(filter(lambda line: line[0].x > corner.x and ((line[0].y <= corner.y <= line[1].y) or (line[1].y <= corner.y <= line[0].y)), outside_vertical_lines),
                                          key=lambda line: abs(line[0].x - corner.x))[0]
                added_horizontal_lines.add(sort_tuple(corner, Coordinates(next_corner_line[0].x, corner.y)))
            elif direction == facing.DOWN:
                next_corner_line = sorted(filter(lambda line: line[0].y > corner.y and ((line[0].x <= corner.x <= line[1].x) or (line[1].x <= corner.x <= line[0].x)), outside_horizontal_lines),
                                          key=lambda line: abs(line[0].y - corner.y))[0]
                added_vertical_lines.add(sort_tuple(corner, Coordinates(corner.x, next_corner_line[0].y)))
            elif direction == facing.UP:
                next_corner_line = sorted(filter(lambda line: line[0].y < corner.y and ((line[0].x <= corner.x <= line[1].x) or (line[1].x <= corner.x <= line[0].x)), outside_horizontal_lines),
                                          key=lambda line: abs(line[0].y - corner.y))[0]
                added_vertical_lines.add(sort_tuple(corner, Coordinates(corner.x, next_corner_line[0].y)))

    # print_lines(added_horizontal_lines, added_vertical_lines, get_min_max(corners)[1])

    for line in outside_horizontal_lines:
        added_horizontal_lines.add(sort_tuple(*line))

    for line in outside_vertical_lines:
        added_vertical_lines.add(sort_tuple(*line))

    print(f"Got a total of {len(added_horizontal_lines)} horizontal lines")
    print(f"Got a total of  {len(added_vertical_lines)} vertical lines")
    return list(added_horizontal_lines), list(added_vertical_lines)


def reorganize_lines(original_horizontal_lines: list[tuple[Coordinates, Coordinates]], original_vertical_lines: list[tuple[Coordinates, Coordinates]]) \
        -> tuple[list[tuple[Coordinates, Coordinates]], list[tuple[Coordinates, Coordinates]]]:

    # TODO make sure the no outer points are connected additionally. Just subdivide lines instead of connecting all points
    all_points = set()
    for line in original_horizontal_lines + original_vertical_lines:
        all_points.add(line[0])
        all_points.add(line[1])

    for horizontal_line in original_horizontal_lines:
        if horizontal_line[0].x < horizontal_line[1].x:
            left = horizontal_line[0]
            right = horizontal_line[1]
        else:
            left = horizontal_line[1]
            right = horizontal_line[0]

        def is_crossing_horizontal_line(vertical_line: tuple[Coordinates, Coordinates]) -> bool:
            if vertical_line[0].y < vertical_line[1].y:
                top = vertical_line[0]
                bottom = vertical_line[1]
            else:
                top = vertical_line[1]
                bottom = vertical_line[0]

            return left.x <= top.x <= right.x and top.y <= left.y <= bottom.y

        crossing_vertical_lines = list(filter(is_crossing_horizontal_line, original_vertical_lines))
        for line in crossing_vertical_lines:
            position_to_add = Coordinates(line[0].x, horizontal_line[0].y)
            all_points.add(position_to_add)

    print(f"{len(all_points)} is the total number of points")
    horizontal_lines = set()
    vertical_lines = set()
    for position in all_points:
        vertical_above = sorted(filter(lambda point: point.x == position.x and point.y < position.y, all_points), key=lambda point: abs(point.y - position.y))
        if len(vertical_above) > 0:
            vertical_lines.add(sort_tuple(vertical_above[0], position))
        vertical_below = sorted(filter(lambda point: point.x == position.x and point.y > position.y, all_points), key=lambda point: abs(point.y - position.y))
        if len(vertical_below) > 0:
            vertical_lines.add(sort_tuple(vertical_below[0], position))

        horizontal_left = sorted(filter(lambda point: point.y == position.y and point.x < position.x, all_points), key=lambda point: abs(point.x - position.x))
        if len(horizontal_left) > 0:
            horizontal_lines.add(sort_tuple(horizontal_left[0], position))
        horizontal_right = sorted(filter(lambda point: point.y == position.y and point.x > position.x, all_points), key=lambda point: abs(point.x - position.x))
        if len(horizontal_right) > 0:
            horizontal_lines.add(sort_tuple(horizontal_right[0], position))

    print(f"Got a total of {len(horizontal_lines)} horizontal lines after considering inside polygon cuts")
    print(f"Got a total of  {len(vertical_lines)} vertical lines after considering inside polygon cuts")
    return list(horizontal_lines), list(vertical_lines)


def find_rectangles(horizontal_lines: list[tuple[Coordinates, Coordinates]], vertical_lines: list[tuple[Coordinates, Coordinates]]) -> list[Rectangle]:
    rectangles = set()
    horizontal_lines.sort(key=lambda line: -line[0].y)
    for line in horizontal_lines:
        rectangle = Rectangle()

        if line[0].x < line[1].x:
            rectangle.bottom_right = line[1]
            rectangle.bottom_left = line[0]
        else:
            rectangle.bottom_right = line[0]
            rectangle.bottom_left = line[1]

        def is_right_line(current_line: tuple[Coordinates, Coordinates]) -> bool:
            return ((current_line[0] == rectangle.bottom_right and rectangle.bottom_right.y > current_line[1].y) or
                    (current_line[1] == rectangle.bottom_right and rectangle.bottom_right.y > current_line[0].y))

        right_line_candidate = list(filter(is_right_line, vertical_lines))
        if len(right_line_candidate) != 1:
            continue
        if right_line_candidate[0][0].y < right_line_candidate[0][1].y:
            rectangle.top_right = right_line_candidate[0][0]
        else:
            rectangle.top_right = right_line_candidate[0][1]

        top_line_candidate = list(filter(lambda current_line: ((current_line[0] == rectangle.top_right and current_line[1].x < rectangle.top_right.x)
                                                               or (current_line[1] == rectangle.top_right and current_line[0].x < rectangle.top_right.x)), horizontal_lines))
        if len(top_line_candidate) != 1:
            continue

        if top_line_candidate[0][0].x < top_line_candidate[0][1].x:
            rectangle.top_left = top_line_candidate[0][0]
        else:
            rectangle.top_left = top_line_candidate[0][1]

        left_line_candidate = list(filter(lambda current_line: ((current_line[0] == rectangle.top_left and current_line[1] == rectangle.bottom_left)
                                                                or (current_line[1] == rectangle.top_left and current_line[0] == rectangle.bottom_left)), vertical_lines))
        if len(left_line_candidate) == 1:
            rectangles.add(rectangle)

    print(f"Found {len(rectangles)} rectangles")
    return list(rectangles)


def print_lines(horizontal_lines: list[tuple[Coordinates, Coordinates]], vertical_lines: list[tuple[Coordinates, Coordinates]], max_coordinates: Coordinates):
    scale_factor = 1000
    scaled_horizontal_lines = [(Coordinates(int(line[0].x / max_coordinates.x * scale_factor), int(line[0].y / max_coordinates.y * scale_factor)),
                                Coordinates(int(line[1].x / max_coordinates.x * scale_factor), int(line[1].y / max_coordinates.y * scale_factor))) for line in horizontal_lines]
    scaled_vertical_lines = [(Coordinates(int(line[0].x / max_coordinates.x * scale_factor), int(line[0].y / max_coordinates.y * scale_factor)),
                              Coordinates(int(line[1].x / max_coordinates.x * scale_factor), int(line[1].y / max_coordinates.y * scale_factor))) for line in vertical_lines]

    grid = {}
    for line in scaled_horizontal_lines:
        diff = line[0].x - line[1].x
        if line[0].x < line[1].x:
            min_x = line[0].x
        else:
            min_x = line[1].x
        for index in range(abs(diff) + 1):
            grid[Coordinates(min_x + index, line[0].y)] = '#'
    for line in scaled_vertical_lines:
        diff = line[0].y - line[1].y
        if line[0].y < line[1].y:
            min_y = line[0].y
        else:
            min_y = line[1].y
        for index in range(abs(diff) + 1):
            grid[Coordinates(line[0].x, min_y + index)] = '#'

    coordinates.print_grid(grid)


facing_grid = {}
color_grid = {}

lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)
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

original_vertical_lines = [(corners[index - 1], corners[index]) for index in range(1, len(corners)) if corners[index - 1].x - corners[index].x == 0]
original_horizontal_lines = [(corners[index - 1], corners[index]) for index in range(1, len(corners)) if corners[index - 1].x - corners[index].x != 0]
inside_corners = find_inside_corners(corners[:-1], original_horizontal_lines)
horizontal_lines, vertical_lines = add_inner_corner_to_outer_border_lines(inside_corners, original_horizontal_lines, original_vertical_lines)
print_lines(horizontal_lines, vertical_lines, get_min_max(corners)[1])
horizontal_lines, vertical_lines = reorganize_lines(horizontal_lines, vertical_lines)
rectangles = find_rectangles(horizontal_lines, vertical_lines)

# print_lines(original_horizontal_lines, original_vertical_lines, get_min_max(corners)[1])
# print_lines(horizontal_lines, vertical_lines, get_min_max(corners)[1])

inside_count = 0
print(f"The total number of pool tiles is {len(facing_grid) + inside_count}.")
