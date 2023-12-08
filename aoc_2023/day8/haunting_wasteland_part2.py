import math
import re

import util.riddle_reader as riddle_reader

COORDINATE_PATTERN = re.compile(r"([A-Z\d]+)\s*=\s*\(([A-Z\d]+)\s*,\s*([A-Z\d]+)\)")


def get_next_position(instruction: str, current_position: str, left: dict[str:str], right: dict[str:str]) -> str:
    if instruction == "L":
        return left[current_position]
    else:
        return right[current_position]


def are_all_positions_final(current_positions: list[str]) -> bool:
    for current_position in current_positions:
        if not current_position.endswith("Z"):
            return False

    return True


def get_number_of_steps(instructions: str, current_position: str, left: dict[str:str], right: dict[str:str], steps_taken: int) -> tuple[int: str]:
    for instruction in instructions:
        steps_taken += 1
        current_position = get_next_position(instruction, current_position, left, right)
        if current_position.endswith("Z"):
            return steps_taken, current_position

    return get_number_of_steps(instructions, current_position, left, right, steps_taken)


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

instructions = lines[0]

# origin coordinate: target coordinate
left = {}
right = {}

starting_positions = []
for index in range(2, len(lines)):
    line = lines[index]
    matcher = COORDINATE_PATTERN.match(line)
    current_position = matcher.group(1)
    left[current_position] = matcher.group(2)
    right[current_position] = matcher.group(3)

    if current_position.endswith("A"):
        starting_positions.append(current_position)

print("left:")
print(left)
print("right:")
print(right)

sequence_lengths = []
for index in range(len(starting_positions)):
    steps_taken = 0
    steps_taken, current_position = get_number_of_steps(instructions, starting_positions[index], left, right, steps_taken=steps_taken)
    print(steps_taken, current_position)
    sequence_lengths.append(steps_taken)

sequence_lengths.sort(reverse=True)
print(sequence_lengths)

print(math.lcm(*sequence_lengths))
print(f"It took {math.lcm(*sequence_lengths)} to reach the target position 'ZZZ'")
