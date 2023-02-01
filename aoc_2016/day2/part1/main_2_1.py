from aoc_2016.day2.common import code_finder
from util.movement.coordinates import Coordinates

KEY_PAD = {Coordinates(value % 3, int(value / 3)): str(value + 1) for value in range(0, 9)}

code_finder.determine_code(Coordinates(1, 1), KEY_PAD)
