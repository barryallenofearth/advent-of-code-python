import math


class Coordinates:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return type(other) == type(self) and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(f"(x={self.x}, y={self.y})")


def distance(coordinates1: Coordinates, coordinates2: Coordinates, count_steps=False):
    if count_steps:
        return math.fabs(coordinates1.x - coordinates2.x) + math.fabs(coordinates1.y - coordinates2.y)
    else:
        return math.sqrt(math.pow(coordinates1.x - coordinates2.x, 2) + math.pow(coordinates1.y - coordinates2.y, 2))


def is_adjacent_to(coordinates1: Coordinates, coordinates2: Coordinates, allow_diagonal=True) -> bool:
    minimum_distance = 1.001
    if allow_diagonal:
        minimum_distance = 1.5

    return distance(coordinates1, coordinates2) < minimum_distance


def is_any_coordinate_adjacent(source_coordinates: Coordinates, coordinates_to_check: list[Coordinates], allow_diagonal=True) -> bool:
    for check in coordinates_to_check:
        if is_adjacent_to(source_coordinates, check, allow_diagonal):
            return True
    return False


# returns a dictionary with keys of coordinates (row, column) = symbol at corresponding position
def read_grid(lines: list[str], column_start=0, row_start=0) -> dict[Coordinates:str]:
    coordinates_with_symbol = {}
    for column in range(column_start, len(lines) + column_start):
        line = lines[column - column_start]
        for row in range(row_start, len(line) + row_start):
            symbol = line[row - row_start]
            coordinates_with_symbol[Coordinates(row, column)] = symbol

    return coordinates_with_symbol


def find_symbols_in_grid(coordinates_with_symbol: dict[Coordinates:str], wanted_symbol: str, equals_check=True) -> list[Coordinates]:
    return [coordinates for coordinates, symbol in coordinates_with_symbol.items() if (symbol == wanted_symbol and equals_check) or (symbol != wanted_symbol and not equals_check)]


# returns a tuple containing 2 coordinates: (x_min, y_min), (x_max, y_max)
def get_min_max_grid_coordinates(grid: list[Coordinates], x_min=10000000000000000000000000000000000000, y_min=10000000000000000000000000000000000000, x_max=-10000000000000000000000000000000000000,
                                 y_max=-10000000000000000000000000000000000000) -> tuple[Coordinates, Coordinates]:
    for position in grid:
        if position.x < x_min:
            x_min = position.x
        if position.x > x_max:
            x_max = position.x
        if position.y < y_min:
            y_min = position.y
        if position.y > y_max:
            y_max = position.y

    return Coordinates(x_min, y_min), Coordinates(x_max, y_max)


def print_grid(grid: dict[Coordinates:str], min_coordinates=None, max_coordinates=None) -> tuple[Coordinates, Coordinates]:
    if min_coordinates is None or max_coordinates is None:
        min_coordinates, max_coordinates = get_min_max_grid_coordinates(grid)

    for column in range(min_coordinates.y, max_coordinates.y + 1):
        for row in range(min_coordinates.x, max_coordinates.x + 1):
            current_coordinates = Coordinates(row, column)
            if current_coordinates in grid:
                print(grid[current_coordinates], end="")
            else:
                print(".", end="")

        print()

    print()

    return min_coordinates, max_coordinates


def is_off_grid(position: Coordinates, min_coordinates: Coordinates, max_coordinates: Coordinates):
    return not (min_coordinates.x <= position.x <= max_coordinates.x and min_coordinates.y <= position.y <= max_coordinates.y)


def find_neighbors_of_symbol(center_coordinates: Coordinates, wanted_symbol: str, coordinates_with_symbol: dict[Coordinates:str], check_diagonally=False) -> list[Coordinates]:
    min_max_coordinates = get_min_max_grid_coordinates(coordinates_with_symbol)

    def is_wanted_symbol(to_check: Coordinates) -> bool:
        return not is_off_grid(to_check, min_max_coordinates[0], min_max_coordinates[1]) and coordinates_with_symbol[to_check] == wanted_symbol

    matching_neighbors = []
    left = Coordinates(center_coordinates.x - 1, center_coordinates.y)
    if is_wanted_symbol(left):
        matching_neighbors.append(left)

    top = Coordinates(center_coordinates.x, center_coordinates.y - 1)
    if is_wanted_symbol(top):
        matching_neighbors.append(top)

    right = Coordinates(center_coordinates.x + 1, center_coordinates.y)
    if is_wanted_symbol(right):
        matching_neighbors.append(right)

    bottom = Coordinates(center_coordinates.x, center_coordinates.y + 1)
    if is_wanted_symbol(bottom):
        matching_neighbors.append(bottom)

    if check_diagonally:

        top_left = Coordinates(center_coordinates.x - 1, center_coordinates.y - 1)
        if is_wanted_symbol(top_left):
            matching_neighbors.append(top_left)

        top_right = Coordinates(center_coordinates.x + 1, center_coordinates.y - 1)
        if is_wanted_symbol(top_right):
            matching_neighbors.append(top_right)

        bottom_right = Coordinates(center_coordinates.x + 1, center_coordinates.y + 1)
        if is_wanted_symbol(bottom_right):
            matching_neighbors.append(bottom_right)

        bottom_left = Coordinates(center_coordinates.x - 1, center_coordinates.y + 1)
        if is_wanted_symbol(bottom_left):
            matching_neighbors.append(bottom_left)

    return matching_neighbors
