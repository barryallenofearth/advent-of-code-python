from aoc_2016.day2.common import read_instructions
from util.movement.coordinates import Coordinates
import util.movement.facing as facing


def determine_code(starting_coordinates: Coordinates, keepad: dict):
    command_rows = read_instructions.read_file()

    current_coordinates = starting_coordinates

    number_sequence = ""
    for row in command_rows:
        for command in row:
            next_coordinates = facing.move_forward(current_coordinates, command, 1)
            if next_coordinates not in keepad:
                continue
            current_coordinates = next_coordinates
        number_sequence += keepad.get(current_coordinates)

    print(f"The bathroom code is {number_sequence}")
