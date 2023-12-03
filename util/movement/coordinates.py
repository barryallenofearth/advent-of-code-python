import math


class Coordinates:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return type(other) == type(self) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


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
