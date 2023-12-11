import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement.coordinates import Coordinates


def count_expanded_coordinates_before(row_or_column_to_expand: list[int], coordinate_part: int) -> int:
    count = 0
    for number in range(coordinate_part + 1):
        if number in row_or_column_to_expand:
            count += 1
    return count


def is_counted_yet(counted: list[tuple[Coordinates:Coordinates]], galaxy: Coordinates, reference: Coordinates):
    for element in counted:
        if (element[0] == galaxy and element[1] == reference) or (element[1] == galaxy and element[0] == reference):
            return True

    return False


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
coordinates_with_symbols = coordinates.read_grid(lines, 1, 1)

rows = [row for row in range(1, len(lines[0]) + 1)]
columns = [column for column in range(1, len(lines) + 1)]

galaxies = coordinates.find_symbols_in_grid(coordinates_with_symbols, "#")
for galaxy in galaxies:
    if galaxy.x in rows:
        rows.remove(galaxy.x)

    if galaxy.y in columns:
        columns.remove(galaxy.y)

print(f"empty rows: {rows}")
print(f"empty rows: {columns}")

expanded_coordinates_with_symbols = {}
max_x = 0
max_y = 0
for position, symbol in coordinates_with_symbols.items():
    rows_expanded_before = count_expanded_coordinates_before(rows, position.x)
    columns_expanded_before = count_expanded_coordinates_before(columns, position.y)

    coordinate = Coordinates(position.x + rows_expanded_before, position.y + columns_expanded_before)
    if coordinate.x > max_x:
        max_x = coordinate.x
    if coordinate.y > max_y:
        max_y = coordinate.y
    expanded_coordinates_with_symbols[coordinate] = symbol

for row in rows:
    for y in range(1, max_y + 1):
        rows_expanded_before = count_expanded_coordinates_before(rows, row) - 1
        expanded_coordinates_with_symbols[Coordinates(row + rows_expanded_before, y)] = "."
for column in columns:
    for x in range(1, max_x + 1):
        rows_expanded_before = count_expanded_coordinates_before(columns, column) - 1
        expanded_coordinates_with_symbols[Coordinates(x, column + rows_expanded_before)] = "."

for column in range(1, max_y + 1):
    for row in range(1, max_x + 1):
        position = Coordinates(row, column)
        if position in expanded_coordinates_with_symbols:
            print(expanded_coordinates_with_symbols[position], end="")
        else:
            print("-", end="")
    print()

galaxies = coordinates.find_symbols_in_grid(expanded_coordinates_with_symbols, "#")
print(f"calcalate distance between {len(galaxies)}")
total_distance = 0
counted = []
for galaxy in galaxies:
    for reference in galaxies:
        if galaxy == reference:
            continue

        distance = coordinates.distance(galaxy, reference, count_steps=True)
        if len(counted) % 1000 == 0:
            print(f"Distance {galaxy} to {reference}: {distance}")
        total_distance += distance
        counted.append((galaxy, reference))

print(f"Total distance: {total_distance/2}")
