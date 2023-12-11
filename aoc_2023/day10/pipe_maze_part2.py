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
                coordinates_with_facing[coordinates1] = next_facing

    current_coordinates = connected_coordinates[-1]
    current_symbol = coordinates_with_symbols[current_coordinates]

    north = Coordinates(current_coordinates.x, current_coordinates.y - 1)
    east = Coordinates(current_coordinates.x + 1, current_coordinates.y)
    south = Coordinates(current_coordinates.x, current_coordinates.y + 1)
    west = Coordinates(current_coordinates.x - 1, current_coordinates.y)

    if current_symbol == "S":
        current_facing = update_starting_symbol(coordinates_with_symbols, current_coordinates, north, east, south, west)
        current_symbol = coordinates_with_symbols[current_coordinates]
        coordinates_with_facing[current_coordinates] = current_facing

    add_if_not_yet_present(current_coordinates, north, facing.UP if current_symbol == "|" or north not in coordinates_with_symbols else coordinates_with_symbols[current_coordinates])
    add_if_not_yet_present(current_coordinates, east, facing.RIGHT if current_symbol == "-" or east not in coordinates_with_symbols else coordinates_with_symbols[current_coordinates])
    add_if_not_yet_present(current_coordinates, south, facing.DOWN if current_symbol == "|" or south not in coordinates_with_symbols else coordinates_with_symbols[current_coordinates])
    add_if_not_yet_present(current_coordinates, west, facing.LEFT if current_symbol == "-" or west not in coordinates_with_symbols else coordinates_with_symbols[current_coordinates])


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
            current_facing = current_symbol
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "J"
            current_facing = current_symbol
    if east_symbol in EAST_SYMBOLS:
        if south_symbol in SOUTH_SYMBOLS:
            current_symbol = "F"
            current_facing = current_symbol
        elif north_symbol in NORTH_SYMBOLS:
            current_symbol = "L"
            current_facing = current_symbol
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "-"
            current_facing = facing.LEFT
    if south_symbol in SOUTH_SYMBOLS:
        if east_symbol in EAST_SYMBOLS:
            current_symbol = "F"
            current_facing = current_symbol
        elif west_symbol in WEST_SYMBOLS:
            current_symbol = "7"
            current_facing = current_symbol

    coordinates_with_symbols[current_coordinates] = current_symbol
    return current_facing


def group_non_border_regions(non_border_coordinates: list[Coordinates], groups: list[list[Coordinates]]):
    remaining = list(non_border_coordinates)
    group = [remaining[0]]
    groups.append(group)
    remaining.remove(group[0])
    is_number_of_elements_different = True
    while is_number_of_elements_different:
        remaining_elements = len(remaining)
        for element in remaining:
            if coordinates.is_any_coordinate_adjacent(element, group, allow_diagonal=False):
                group.append(element)

        for member in group:
            if member in remaining:
                remaining.remove(member)

        is_number_of_elements_different = remaining_elements != len(remaining)

    if len(remaining) != 0:
        group_non_border_regions(remaining, groups)


def is_right_of_path_up(region_group: list[Coordinates], coordinates_with_facing: [dict[Coordinates:str]], connected_coordinates: list[Coordinates]) -> tuple[
    bool, Coordinates, Coordinates, str, Coordinates]:
    is_right_of_path = None
    up_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.UP)
    matching_position = None
    matching_facing = None
    border_coordinate = None
    previous_coordinate = None
    for position in up_symbols:
        if is_right_of_path is not None:
            break
        if connected_coordinates.index(position) < 2:
            continue
        for region_element in region_group:
            if Coordinates(position.x + 1, position.y) == region_element:
                is_right_of_path = True
                matching_position = position
                matching_facing = facing.UP
                border_coordinate = region_element
                break
            elif Coordinates(position.x - 1, position.y) == region_element:
                is_right_of_path = False
                matching_position = position
                matching_facing = facing.UP
                border_coordinate = region_element
                break

    if is_right_of_path is None:
        down_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.DOWN)
        for position in down_symbols:
            if is_right_of_path is not None:
                break
            if connected_coordinates.index(position) < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x - 1, position.y) == region_element:
                    is_right_of_path = True
                    matching_position = position
                    matching_facing = facing.DOWN
                    border_coordinate = region_element
                    break
                elif Coordinates(position.x + 1, position.y) == region_element:
                    is_right_of_path = False
                    matching_position = position
                    matching_facing = facing.DOWN
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        right_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.RIGHT)
        for position in right_symbols:
            if is_right_of_path is not None:
                break
            if connected_coordinates.index(position) < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x, position.y + 1) == region_element:
                    is_right_of_path = True
                    matching_position = position
                    matching_facing = facing.RIGHT
                    border_coordinate = region_element
                    break
                elif Coordinates(position.x, position.y - 1) == region_element:
                    is_right_of_path = False
                    matching_position = position
                    matching_facing = facing.RIGHT
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        left_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, facing.LEFT)
        for position in left_symbols:
            if is_right_of_path is not None:
                break
            if connected_coordinates.index(position) < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x, position.y - 1) == region_element:
                    is_right_of_path = True
                    matching_position = position
                    matching_facing = facing.LEFT
                    border_coordinate = region_element
                    break
                elif Coordinates(position.x, position.y + 1) == region_element:
                    is_right_of_path = False
                    matching_position = position
                    matching_facing = facing.LEFT
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        seven_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, "7")
        for position in seven_symbols:
            if is_right_of_path is not None:
                break
            index = connected_coordinates.index(position)
            if index < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x + 1, position.y) == region_element or Coordinates(position.x, position.y - 1) == region_element:
                    previous_coordinate = connected_coordinates[index - 1]
                    # is previous coordinate below 7
                    is_right_of_path = previous_coordinate.x == position.x and previous_coordinate.y - 1 == position.y
                    matching_position = position
                    matching_facing = "7"
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        f_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, "F")
        for position in f_symbols:
            if is_right_of_path is not None:
                break
            index = connected_coordinates.index(position)
            if index < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x - 1, position.y) == region_element or Coordinates(position.x, position.y - 1) == region_element:
                    previous_coordinate = connected_coordinates[index - 1]
                    # is previous coordinate right next to F
                    is_right_of_path = previous_coordinate.x - 1 == position.x and previous_coordinate.y == position.y
                    matching_position = position
                    matching_facing = "F"
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        j_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, "J")
        for position in j_symbols:
            if is_right_of_path is not None:
                break
            index = connected_coordinates.index(position)
            if index < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x + 1, position.y) == region_element or Coordinates(position.x, position.y + 1) == region_element:
                    previous_coordinate = connected_coordinates[index - 1]
                    # is previous coordinate left of J
                    is_right_of_path = previous_coordinate.x + 1 == position.x and previous_coordinate.y == position.y

                    matching_position = position
                    matching_facing = "J"
                    border_coordinate = region_element
                    break

    if is_right_of_path is None:
        l_symbols = coordinates.find_symbols_in_grid(coordinates_with_facing, "L")
        for position in l_symbols:
            if is_right_of_path is not None:
                break
            index = connected_coordinates.index(position)
            if index < 2:
                continue
            for region_element in region_group:
                if Coordinates(position.x - 1, position.y) == region_element or Coordinates(position.x, position.y + 1) == region_element:
                    previous_coordinate = connected_coordinates[index - 1]
                    # is previous coordinate above L
                    is_right_of_path = previous_coordinate.x == position.x and previous_coordinate.y + 1 == position.y
                    matching_position = position
                    matching_facing = "L"
                    border_coordinate = region_element
                    break

    return is_right_of_path, matching_position, previous_coordinate, matching_facing, border_coordinate


def filter_for_neighbors(group: list[Coordinates], coordinates_with_facings: dict[Coordinates:str], add_neighbors_of_neighbors=True) -> dict[Coordinates:str]:
    neighbors_to_group = {}
    for position in group:
        north = Coordinates(position.x, position.y - 1)
        east = Coordinates(position.x + 1, position.y)
        south = Coordinates(position.x, position.y + 1)
        west = Coordinates(position.x - 1, position.y)

        if north in coordinates_with_facings:
            neighbors_to_group[north] = coordinates_with_facings[north]
        if south in coordinates_with_facings:
            neighbors_to_group[south] = coordinates_with_facings[south]
        if east in coordinates_with_facings:
            neighbors_to_group[east] = coordinates_with_facings[east]
        if west in coordinates_with_facings:
            neighbors_to_group[west] = coordinates_with_facings[west]

    if add_neighbors_of_neighbors:
        neighbors_to_group.update(filter_for_neighbors([neighbour for neighbour, symbol in neighbors_to_group.items()], coordinates_with_facings, add_neighbors_of_neighbors=False))
    return neighbors_to_group


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
coordinates_with_symbols = coordinates.read_grid(lines, row_start=1, column_start=1)
starting_position = coordinates.find_symbols_in_grid(coordinates_with_symbols, "S")[0]

print(f"starting position: {starting_position}")

connected_coordinates = [starting_position]
coordinates_with_facing = {}
was_symbol_added = True
while was_symbol_added:
    previous_length = len(connected_coordinates)
    get_symbol_neighbours(coordinates_with_symbols, connected_coordinates, coordinates_with_facing)
    was_symbol_added = len(connected_coordinates) != previous_length

print(f"The path length is {math.ceil(len(connected_coordinates) / 2)}")

for position, symbol in coordinates_with_symbols.items():
    if position not in connected_coordinates:
        coordinates_with_symbols[position] = "."
    else:
        coordinates_with_symbols[position] = symbol

all_empty_spaces = coordinates.find_symbols_in_grid(coordinates_with_symbols, ".")


def is_not_in_contact_with_border(empty_coordinates: Coordinates, x_min=1, x_max=len(lines[0]), y_min=1, y_max=len(lines)) -> bool:
    return empty_coordinates.x != x_min and empty_coordinates.x != x_max and empty_coordinates.y != y_min and empty_coordinates.y != y_max


def is_in_contact_with_border(empty_coordinates: Coordinates) -> bool:
    return not is_not_in_contact_with_border(empty_coordinates)


remaining_empty_coordinates = list(all_empty_spaces)
border_region = list(filter(is_in_contact_with_border, all_empty_spaces))

nodes_added_to_border_region = True
previous_node_count = 0
while nodes_added_to_border_region:

    for test_coordinate in remaining_empty_coordinates:
        if test_coordinate not in border_region:
            if coordinates.is_any_coordinate_adjacent(test_coordinate, border_region, allow_diagonal=False):
                border_region.append(test_coordinate)

    for value in border_region:
        if value in remaining_empty_coordinates:
            remaining_empty_coordinates.remove(value)

    nodes_added_to_border_region = previous_node_count != len(border_region)
    previous_node_count = len(border_region)

print("Pipe main loop after cleanup")
for column in range(1, len(lines) + 1):
    for row in range(1, len(lines[0]) + 1):
        current_coordinates = Coordinates(row, column)
        if current_coordinates in connected_coordinates:
            print(coordinates_with_symbols[current_coordinates], end="")
        elif current_coordinates in border_region:
            print(".", end="")
        else:
            print("#", end="")
    print()

print("\nFacings")
for column in range(1, len(lines) + 1):
    for row in range(1, len(lines[0]) + 1):
        current_coordinates = Coordinates(row, column)
        if current_coordinates in coordinates_with_facing:
            print(coordinates_with_facing[current_coordinates], end="")
        elif current_coordinates in border_region:
            print(".", end="")
        else:
            print("#", end="")
    print()

all_non_border_regions = [empty_coordinate for empty_coordinate in all_empty_spaces if empty_coordinate not in border_region]
print(f"Empty spaces in border region: {border_region}, #: {len(border_region)}")
print(f"Empty spaces not in border region: {all_non_border_regions}, #: {len(all_non_border_regions)}")

groups = []
group_non_border_regions(all_non_border_regions, groups)
print(f"{len(groups)} groups of non border contacts could be identified")

is_border_right_of_path_up, matching_position, previous_coordinate, matching_facing, border_coordinate = is_right_of_path_up(border_region, coordinates_with_facing, connected_coordinates)
print(f"Border is {'right' if is_border_right_of_path_up else 'left'} of path up")
print(f"Matching position: {matching_position}='{matching_facing}' (previous coordinate: {previous_coordinate} ) connected to border region {border_coordinate}")
inside_groups = []
for group in groups:
    print(f"Testing group {groups.index(group)}/{len(groups)} containing {len(group)} empty spots")
    neighbors_to_group = filter_for_neighbors(group, coordinates_with_facing)
    is_group_right_of_path_up, matching_position, previous_coordinate, matching_facing, border_coordinate = is_right_of_path_up(group, neighbors_to_group, connected_coordinates)
    print(f"Group is {'right' if is_group_right_of_path_up else 'left'} of path up")
    print(f"Matching position: {matching_position}='{matching_facing}' (previous coordinate: {previous_coordinate} ) connected to border region {border_coordinate}")
    if (is_group_right_of_path_up and not is_border_right_of_path_up) or (not is_group_right_of_path_up and is_border_right_of_path_up):
        inside_groups.append(group)
        print(group)

print(f"{len(inside_groups)} groups are inside the border")
print(f"{reduce(lambda count, l: count + len(l), inside_groups, 0)} empty spaces are inside the border")
