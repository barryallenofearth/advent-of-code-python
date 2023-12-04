import re

import util.riddle_reader as riddle_reader
import util.movement.coordinates as coordinates

NUMBERS_PATTERN = re.compile(r"(\d+)")
SYMBOL_PATTERN = re.compile(r"[^\d.]")

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)


class NumberWithCoordinates:

    def __init__(self, number: str, row: int, starting_column: int):
        self.number = int(number)

        self.coordinates = [coordinates.Coordinates(row, column) for column in range(starting_column, starting_column + len(number))]
        self.processed = False

    def __repr__(self):
        return f"{self.number}: [{','.join([coordinate.__str__() for coordinate in self.coordinates])}]"


def generate_dots_of_equal_length(original_string: str):
    return "".join(["." for symbol in original_string])


numbers_with_coordinates = []
symbol_coordinates = []
row = 1
for line in lines:
    all_numbers = NUMBERS_PATTERN.findall(line)
    for number in all_numbers:
        start_column = line.index(number) + 1
        numbers_with_coordinates.append(NumberWithCoordinates(number, row, start_column))
        line = line.replace(number, generate_dots_of_equal_length(number), 1)

    for column in range(len(line)):
        if SYMBOL_PATTERN.match(line[column]):
            symbol_coordinates.append(coordinates.Coordinates(row, column + 1))
    row += 1

sum = 0
count = 0
for number_with_coordinates in numbers_with_coordinates:
    for symbol in symbol_coordinates:

        if not (symbol.x - 1 <= number_with_coordinates.coordinates[0].x <= symbol.x + 1):
            continue
        if not number_with_coordinates.processed:
            if coordinates.is_any_coordinate_adjacent(symbol, number_with_coordinates.coordinates, allow_diagonal=True):
                print(f"{number_with_coordinates} is adjacent to symbol at {symbol}")
                sum += number_with_coordinates.number
                count += 1
                number_with_coordinates.processed = True

print(f"The total number is {sum}, having found {count} part numbers.")

# for number in numbers_with_coordinates:
#     if not number.processed:
#         print(number)
# for number in numbers_with_coordinates:
#    print(number)
# for symbol in symbol_coordinates:
#    print(symbol)
