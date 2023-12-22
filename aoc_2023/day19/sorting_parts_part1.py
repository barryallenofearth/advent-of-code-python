import re

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

OBJECT_PATTERN = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
INSTRUCTION_PATTERN = re.compile(r"([xmas])([<>])(\d+):([a-z]+|R|A)|([a-z]+|R|A)")
OBJECTS = []
WORKFLOWS = {}


class Instruction:

    def __init__(self, key: str, comparison_value: int, success_target: str, method):
        self.key = key
        self.comparison_value = comparison_value
        self.success_target = success_target
        self.method = method

    def evaluate(self, object: dict[str:int]):
        if self.method is None:
            return self.success_target

        return self.method(object, self.key, self.comparison_value, self.success_target)

    def __repr__(self):
        return f"Instruction: key: {self.key}, comparison_value: {self.comparison_value}, method: {self.method}, success_target: {self.success_target}"


def less_than(object: dict[str:int], key: str, comparison_value: int, success_target) -> str | None:
    if object[key] < comparison_value:
        return success_target
    return None


def more_than(object: dict[str:int], key: str, comparison_value: int, success_target) -> str | None:
    if object[key] > comparison_value:
        return success_target
    return None


def process_workflow(instructions: list[Instruction], object: {dict: int}) -> str:
    for instruction in instructions:
        result = instruction.evaluate(object)
        if result is not None:
            return result

    raise ValueError(f"No result could be found for {object} with the instructions {instructions}")


for line in lines:
    if len(line) == 0:
        continue

    object_match = OBJECT_PATTERN.match(line)
    if object_match:
        OBJECTS.append({"x": int(object_match.group(1)), "m": int(object_match.group(2)), "a": int(object_match.group(3)), "s": int(object_match.group(4))})
    else:
        name = line[:line.index("{")]
        instruction_strings = line[line.index("{") + 1:line.index("}")].split(",")
        instructions = []
        WORKFLOWS[name] = instructions
        for instruction_string in instruction_strings:
            match = INSTRUCTION_PATTERN.match(instruction_string)
            if match:
                if match.group(5) is not None:
                    instructions.append(Instruction("", 0, match.group(5), None))
                else:
                    instructions.append(Instruction(match.group(1), int(match.group(3)), match.group(4), less_than if match.group(2) == "<" else more_than))

total_acceptance = 0
part_count = 0
for object in OBJECTS:
    result = process_workflow(WORKFLOWS["in"], object)
    while result != "A" and result != "R":
        result = process_workflow(WORKFLOWS[result], object)

    if result == "A":
        part_count += 1
        total_acceptance += sum(object.values())

print(f"Total acceptance sum: {total_acceptance}. {part_count} were accepted")
