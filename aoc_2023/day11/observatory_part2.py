import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement.coordinates import Coordinates


def count_expanded_coordinates_before(row_or_column_to_expand: list[int], coordinate_part: int) -> int:
    count = 0
    for number in range(coordinate_part + 1):
        if number in row_or_column_to_expand:
            count += 1
    return count


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
increment_factor = 1000000
for position, symbol in coordinates_with_symbols.items():
    rows_expanded_before = count_expanded_coordinates_before(rows, position.x) * (increment_factor - 1)
    columns_expanded_before = count_expanded_coordinates_before(columns, position.y) * (increment_factor - 1)

    coordinate = Coordinates(position.x + rows_expanded_before, position.y + columns_expanded_before)
    if coordinate.x > max_x:
        max_x = coordinate.x
    if coordinate.y > max_y:
        max_y = coordinate.y
    expanded_coordinates_with_symbols[coordinate] = symbol

if increment_factor <= 100:
    for column in range(1, max_y + 1):
        for row in range(1, max_x + 1):
            position = Coordinates(row, column)
            if position in expanded_coordinates_with_symbols:
                print(expanded_coordinates_with_symbols[position], end="")
            else:
                print("-", end="")
        print()
print(max_x, max_y)
galaxies = coordinates.find_symbols_in_grid(expanded_coordinates_with_symbols, "#")
print(f"calcalate distance between {len(galaxies)} galaxies")
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

print(f"Total distance: {total_distance / 2}")
