import re

import util.riddle_reader as riddle_reader

COORDINATE_PATTERN = re.compile(r"([A-Z\d]+)\s*=\s*\(([A-Z\d]+)\s*,\s*([A-Z\d]+)\)")


def are_all_positions_final(current_positions: list[str]) -> bool:
    for current_position in current_positions:
        if not current_position.endswith("Z"):
            return False

    return True


def get_number_of_steps(instructions: str, left: dict[str:str], right: dict[str:str], current_positions: list[str], steps_taken=0) -> tuple[int: list[str]]:
    for instruction in instructions:
        steps_taken += 1
        for index in range(len(current_positions)):

            if instruction == "L":
                current_positions[index] = left[current_positions[index]]
            else:
                current_positions[index] = right[current_positions[index]]

        if are_all_positions_final(current_positions):
            break

    return steps_taken, current_positions


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

instructions = lines[0]

# origin coordinate: target coordinate
left = {}
right = {}

current_positions = []
for index in range(2, len(lines)):
    line = lines[index]
    matcher = COORDINATE_PATTERN.match(line)
    current_position = matcher.group(1)
    left[current_position] = matcher.group(2)
    right[current_position] = matcher.group(3)

    if current_position.endswith("A"):
        current_positions.append(current_position)

print("left:")
print(left)
print("right:")
print(right)

steps_taken = 0
while not are_all_positions_final(current_positions):
    steps_taken, current_positions = get_number_of_steps(instructions, left, right, current_positions, steps_taken=steps_taken)

print(f"It took {steps_taken} to reach the target position 'ZZZ'")
