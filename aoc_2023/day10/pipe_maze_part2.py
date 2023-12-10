import math
from functools import reduce

import util.riddle_reader as riddle_reader
import util.movement.coordinates as coordinates
from util.movement.coordinates import Coordinates
import util.movement.facing as facing

NORTH_SYMBOLS = ["|", "7", "F"]
SOUTH_SYMBOLS = ["|", "J", "L"]
WEST_SYMBOLS = ["-", "F", "L"]
EAST_SYMBOLS = ["-", "J", "7"]


def are_pipes_connected(coordinates1: Coordinates, coordinates2: Coordinates, coordinates_with_symbols: dict[Coordinates, str]) -> bool:
    coordinates1_symbol = coordinates_with_symbols[coordinates1]
    coordinates2_symbol = coordinates_with_symbols[coordinates2] if coordinates2 in coordinates_with_symbols else None
    # coordinates 2 north of coordinates 1
    if coordinates1.x == coordinates2.x and coordinates1.y > coordinates2.y:
        return coordinates1_symbol in SOUTH_SYMBOLS and coordinates2_symbol in NORTH_SYMBOLS
    # coordinates 2 east of coordinates 1
    elif coordinates1.x < coordinates2.x and coordinates1.y == coordinates2.y:
        return coordinates1_symbol in WEST_SYMBOLS and coordinates2_symbol in EAST_SYMBOLS
    # coordinates 2 south of coordinates 1
    elif coordinates1.x == coordinates2.x and coordinates1.y < coordinates2.y:
        return coordinates1_symbol in NORTH_SYMBOLS and coordinates2_symbol in SOUTH_SYMBOLS
    # coordinates 2 west of coordinates 1
    elif coordinates1.x > coordinates2.x and coordinates1.y == coordinates2.y:
        return coordinates1_symbol in EAST_SYMBOLS and coordinates2_symbol in WEST_SYMBOLS


def get_symbol_neighbours(coordinates_with_symbols: dict[Coordinates, str], connected_coordinates: list[Coordinates], coordinates_with_facing: dict[Coordinates:str]):
    def add_if_not_yet_present(coordinates1: Coordinates, coordinates2: Coordinates, next_facing: str):
        if coordinates2 not in connected_coordinates:
            if are_pipes_connected(coordinates1, coordinates2, coordinates_with_symbols):
                connected_coordinates.append(coordinates2)
                coordinates_with_facing[coordinates2] = next_facing

    current_coordinates = connected_coordinates[-1]
    current_symbol = coordinates_with_symbols[current_coordinates]

    north = Coordinates(current_coordinates.x, current_coordinates.y - 1)
    east = Coordinates(current_coordinates.x + 1, current_coordinates.y)
    south = Coordinates(current_coordinates.x, current_coordinates.y + 1)
    west = Coordinates(current_coordinates.x - 1, current_coordinates.y)

    if current_symbol == "S":
        current_facing = update_starting_symbol(coordinates_with_symbols, current_coordinates, north, east, south, west)
        coordinates_with_facing[current_coordinates] = current_facing

    add_if_not_yet_present(current_coordinates, north, facing.UP)
    add_if_not_yet_present(current_coordinates, east, facing.RIGHT)
    add_if_not_yet_present(current_coordinates, south, facing.DOWN)
    add_if_not_yet_present(current_coordinates, west, facing.LEFT)


def update_starting_symbol(coordinates_with_symbols: dict[Coordinates:str], current_coordinates: Coordinates, north: Coordinates, east: Coordinates, south: Coordinates, west: Coordinates) -> str:
    current_symbol = coordinates_with_symbols[current_coordinates]
    north_symbol = None
    east_symbol = None
    south_symbol = None
    west_symbol = None
    if north in coordinates_with_symbols:
        north_symbol = coordinates_with_symbols[north]
    if east in coordinates_with_symbols:
        east_symbol = coordinates_with_symbols[east]
    if south in coordinates_with_symbols:
        south_symbol = coordinates_with_symbols[south]
    if west in coordinates_with_symbols:
        west_symbol = coordinates_with_symbols[west]

    current_facing = facing.UP
    if north_symbol in NORTH_SYMBOLS:
        if south_symbol in SOUTH_SYMBOLS:
            current_symbol = "|"
            current_facing = facing.UP
        elif east_symbol in EAST_SYMBOLS:
            current_symbol = "L"
            current_facing = facing.DOWN
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "J"
            current_facing = facing.DOWN
    if east_symbol in EAST_SYMBOLS:
        if south_symbol in SOUTH_SYMBOLS:
            current_symbol = "F"
            current_facing = facing.RIGHT
        elif north_symbol in NORTH_SYMBOLS:
            current_symbol = "L"
            current_facing = facing.DOWN
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "-"
            current_facing = facing.LEFT
    if south_symbol in SOUTH_SYMBOLS:
        if east_symbol in EAST_SYMBOLS:
            current_symbol = "F"
            current_facing = facing.LEFT
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "7"
            current_facing = facing.RIGHT

    coordinates_with_symbols[current_coordinates] = current_symbol
    return current_facing


def group_non_boarder_regions(non_boarder_coordinates: list[Coordinates], groups: list[list[Coordinates]]):
    remaining = list(non_boarder_coordinates)
    group = [remaining[0]]
    groups.append(group)
    remaining.remove(group[0])
    for element in remaining:
        if coordinates.is_any_coordinate_adjacent(element, group):
            group.append(element)

    for member in group:
        if member in remaining:
            remaining.remove(member)

    if len(remaining) != 0:
        group_non_boarder_regions(remaining, groups)


def is_right_of_path_up(region_group: list[Coordinates], coordinates_with_facing: [dict[Coordinates:str]], connected_coordinates: list[Coordinates])->bool:
    is_right_of_path = None
    down_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.UP)
    for position in down_symbols:
        if connected_coordinates.index(position) < 2:
            continue
        for border in region_group:
            if Coordinates(position.x + 1, position.y) == border:
                is_right_of_path = True
                break
            elif Coordinates(position.x - 1, position.y) == border:
                is_right_of_path = False
                break

    if is_right_of_path is None:
        up_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.UP)
        for position in up_symbols:
            if connected_coordinates.index(position) < 2:
                continue
            for border in region_group:
                if Coordinates(position.x - 1, position.y) == border:
                    is_right_of_path = True
                    break
                elif Coordinates(position.x + 1, position.y) == border:
                    is_right_of_path = False
                    break

    if is_right_of_path is None:
        right_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.RIGHT)
        for position in right_symbols:
            if connected_coordinates.index(position) < 2:
                continue
            for border in region_group:
                if Coordinates(position.x, position.y - 1) == border:
                    is_right_of_path = True
                    break
                elif Coordinates(position.x, position.y + 1) == border:
                    is_right_of_path = False
                    break

    if is_right_of_path is None:
        left_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.LEFT)
        for position in left_symbols:
            if connected_coordinates.index(position) < 2:
                continue
            for border in region_group:
                if Coordinates(position.x, position.y + 1) == border:
                    is_right_of_path = True
                    break
                elif Coordinates(position.x, position.y - 1) == border:
                    is_right_of_path = False
                    break

    return is_right_of_path


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
coordinates_with_symbols = coordinates.read_grid(lines, row_start=1, column_start=1)
starting_position = coordinates.find_symbols_in_grid(coordinates_with_symbols, "S")[0]

print(f"starting position: {starting_position}")

all_empty_spaces = coordinates.find_symbols_in_grid(coordinates_with_symbols, ".")


def is_not_in_contact_with_boarder(empty_coordinates: Coordinates, x_min=1, x_max=len(lines[0]), y_min=1, y_max=len(lines)) -> bool:
    return empty_coordinates.x != x_min and empty_coordinates.x != x_max and empty_coordinates.y != y_min and empty_coordinates.y != y_max


def is_in_contact_with_boarder(empty_coordinates: Coordinates) -> bool:
    return not is_not_in_contact_with_boarder(empty_coordinates)


remaining_empty_coordinates = list(all_empty_spaces)
border_region = list(filter(is_in_contact_with_boarder, all_empty_spaces))

nodes_added_to_boarder_region = True
previous_node_count = 0
while nodes_added_to_boarder_region:

    for test_coordinate in remaining_empty_coordinates:
        if test_coordinate not in border_region:
            if coordinates.is_any_coordinate_adjacent(test_coordinate, border_region, allow_diagonal=False):
                border_region.append(test_coordinate)

    for value in border_region:
        if value in remaining_empty_coordinates:
            remaining_empty_coordinates.remove(value)

    nodes_added_to_boarder_region = previous_node_count != len(border_region)
    previous_node_count = len(border_region)

all_non_boarder_regions = [empty_coordinate for empty_coordinate in all_empty_spaces if empty_coordinate not in border_region]
print(f"Empty spaces in boarder region: {border_region}, #: {len(border_region)}")
print(f"Empty spaces not in boarder region: {all_non_boarder_regions}, #: {len(all_non_boarder_regions)}")

groups = []
group_non_boarder_regions(all_non_boarder_regions, groups)
print(f"{len(groups)} groups of non boarder contacts could be identified")

connected_coordinates = [starting_position]
coordinates_with_facing = {}
was_symbol_added = True
while was_symbol_added:
    previous_length = len(connected_coordinates)
    get_symbol_neighbours(coordinates_with_symbols, connected_coordinates, coordinates_with_facing)
    was_symbol_added = len(connected_coordinates) != previous_length

print(connected_coordinates)

print(f"The path length is {math.ceil(len(connected_coordinates) / 2)}")

for row in range(1, len(lines[0]) + 2):
    for column in range(1, len(lines) + 2):
        current_coordinates = Coordinates(column, row)
        if current_coordinates in connected_coordinates:
            print(coordinates_with_facing[current_coordinates], end="")
        else:
            print(".", end="")

    print()

is_border_right_of_path_up = is_right_of_path_up(border_region, coordinates_with_facing, connected_coordinates)
inside_groups = []
for group in groups:
    is_group_right_of_path_up = is_right_of_path_up(group, coordinates_with_facing, connected_coordinates)
    if (is_group_right_of_path_up and not is_border_right_of_path_up) or (not is_group_right_of_path_up and is_border_right_of_path_up):
        inside_groups.append(group)

print(f"{len(inside_groups)} are inside the border")
print(f"{reduce(lambda count, l: count + len(l), inside_groups, 0)} are inside the border")
