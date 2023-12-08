import re

import util.riddle_reader as riddle_reader

COORDINATE_PATTERN = re.compile(r"([A-Z]+)\s*=\s*\(([A-Z]+)\s*,\s*([A-Z]+)\)")


def get_number_of_steps(instructions: str, left: dict[str:str], right: dict[str:str], current_position="AAA", steps_taken=0) -> int:
    target_position = "ZZZ"
    for instruction in instructions:
        steps_taken += 1
        if instruction == "L":
            current_position = left[current_position]
        else:
            current_position = right[current_position]

        if current_position == target_position:
            break

    if current_position != target_position:
        return get_number_of_steps(instructions, left, right, current_position, steps_taken)
    else:
        return steps_taken


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

instructions = lines[0]

# origin coordinate: target coordinate
left = {}
right = {}
for index in range(2, len(lines)):
    line = lines[index]
    matcher = COORDINATE_PATTERN.match(line)
    left[matcher.group(1)] = matcher.group(2)
    right[matcher.group(1)] = matcher.group(3)

print("left:")
print(left)
print("right:")
print(right)

steps_taken = get_number_of_steps(instructions, left, right)
print(f"It took {steps_taken} to reach the target position 'ZZZ'")
