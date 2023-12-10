import math

import util.riddle_reader as riddle_reader
import util.movement.coordinates as coordinates

NORTH_SYMBOLS = ["|", "7", "F"]
SOUTH_SYMBOLS = ["|", "J", "L"]
WEST_SYMBOLS = ["-", "F", "L"]
EAST_SYMBOLS = ["-", "J", "7"]



def get_symbol_neighbours(coordinates_with_symbols: dict[coordinates.Coordinates, str], connected_coordinates: list[coordinates.Coordinates]):
    current_coordinates = connected_coordinates[-1]
    current_symbol = coordinates_with_symbols[current_coordinates]

    north = coordinates.Coordinates(current_coordinates.x, current_coordinates.y - 1)
    east = coordinates.Coordinates(current_coordinates.x + 1, current_coordinates.y)
    south = coordinates.Coordinates(current_coordinates.x, current_coordinates.y + 1)
    west = coordinates.Coordinates(current_coordinates.x - 1, current_coordinates.y)

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

    current_symbol = update_starting_symbol(coordinates_with_symbols, current_coordinates, current_symbol, east_symbol, north_symbol, south_symbol, west_symbol)

    if current_symbol in SOUTH_SYMBOLS and north_symbol in NORTH_SYMBOLS:
        if north not in connected_coordinates:
            connected_coordinates.append(north)
    if current_symbol in NORTH_SYMBOLS and south_symbol in SOUTH_SYMBOLS:
        if south not in connected_coordinates:
            connected_coordinates.append(south)
    if current_symbol in EAST_SYMBOLS and west_symbol in WEST_SYMBOLS:
        if west not in connected_coordinates:
            connected_coordinates.append(west)
    if current_symbol in WEST_SYMBOLS and east_symbol in EAST_SYMBOLS:
        if east not in connected_coordinates:
            connected_coordinates.append(east)


def update_starting_symbol(coordinates_with_symbols, current_coordinates, current_symbol, east_symbol, north_symbol, south_symbol, west_symbol):
    if current_symbol == "S":
        if north_symbol in NORTH_SYMBOLS:
            if south_symbol in SOUTH_SYMBOLS:
                current_symbol = "|"
            elif east_symbol in EAST_SYMBOLS:
                current_symbol = "L"
            elif west_symbol in WEST_SYMBOLS:
                current_symbol = "J"
        if east_symbol in EAST_SYMBOLS:
            if south_symbol in SOUTH_SYMBOLS:
                current_symbol = "F"
            elif north_symbol in NORTH_SYMBOLS:
                current_symbol = "L"
            elif west_symbol in WEST_SYMBOLS:
                current_symbol = "-"
        if south_symbol in SOUTH_SYMBOLS:
            if east_symbol in EAST_SYMBOLS:
                current_symbol = "F"
            elif west_symbol in WEST_SYMBOLS:
                current_symbol = "7"
    coordinates_with_symbols[current_coordinates] = current_symbol
    return current_symbol


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
coordinates_with_symbols = coordinates.read_grid(lines, row_start=1, column_start=1)
starting_position = coordinates.find_symbols_in_grid(coordinates_with_symbols, "S")[0][0]

print(starting_position)

connected_coordinates = [starting_position]
was_symbol_added = True
while was_symbol_added:
    previous_length = len(connected_coordinates)
    get_symbol_neighbours(coordinates_with_symbols, connected_coordinates)
    was_symbol_added = len(connected_coordinates) != previous_length

print(connected_coordinates)

print(f"The path length is {math.ceil(len(connected_coordinates) / 2)}")
