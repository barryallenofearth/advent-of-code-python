import re
from collections import defaultdict

import util.riddle_reader as riddle_reader


def get_index_of_sequence(lenses: list[tuple[str, int]], wanted_sequence: str) -> int:
    for index, lens in enumerate(lenses):
        lens_sequence = lens[0]
        if lens_sequence == wanted_sequence:
            return index

    return -1


INSTRUCTION_PATTERN = re.compile("^(.+)([\-=])(\d+)?$")

line = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)[0]

sequences = line.split(",")
boxes_with_lenses = defaultdict(list)
for instruction in sequences:
    print(instruction)
    matcher = INSTRUCTION_PATTERN.match(instruction)
    sequence = matcher.group(1)
    operation = matcher.group(2)
    box_id = 0
    for symbol in sequence:
        box_id += ord(symbol)
        box_id *= 17
        box_id = box_id % 256

    lenses = boxes_with_lenses[box_id]
    if operation == "-":
        index = get_index_of_sequence(lenses, sequence)
        if index != -1:
            del lenses[index]

    elif operation == "=":
        focal_length = int(matcher.group(3))
        lens = (sequence, focal_length)
        index = get_index_of_sequence(lenses, sequence)
        if index == -1:
            lenses.append(lens)
        else:
            del lenses[index]
            lenses.insert(index, lens)

total_focussing_power = 0
for box_id, lenses in boxes_with_lenses.items():
    for index, lens in enumerate(lenses):
        lens_focussing_power = 1 + box_id
        lens_focussing_power *= (index + 1)
        lens_focussing_power *= lens[1]
        total_focussing_power += lens_focussing_power
        # print(f"Box {box_id}, slot {index - 1}, focal_strength {lens[1]}: {lens_focussing_power}")

print(f"All boxes: {total_focussing_power}")
