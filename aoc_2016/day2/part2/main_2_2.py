from aoc_2016.day2.common import code_finder
from util.movement.coordinates import Coordinates

KEY_PAD = {Coordinates(2, 0): "1",
           Coordinates(1, 1): "2", Coordinates(2, 1): "3", Coordinates(3, 1): "4",
           Coordinates(0, 2): "5", Coordinates(1, 2): "6", Coordinates(2, 2): "7", Coordinates(3, 2): "8",
           Coordinates(4, 2): "9",
           Coordinates(1, 3): "A", Coordinates(2, 3): "B", Coordinates(3, 3): "C",
           Coordinates(2, 4): "D"}

code_finder.determine_code(Coordinates(0, 2), KEY_PAD)
