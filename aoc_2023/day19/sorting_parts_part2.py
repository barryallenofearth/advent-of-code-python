import re

import util.riddle_reader as riddle_reader

INVALID_RANGE = (0, 0)

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

INSTRUCTION_PATTERN = re.compile(r"([xmas])([<>])(\d+):([a-z]+|R|A)|([a-z]+|R|A)")
OBJECTS = []
WORKFLOWS = {}


class Instruction:

    def __init__(self, key: str, comparison_value: int, success_target: str, symbol: str):
        self.key = key
        self.comparison_value = comparison_value
        self.success_target = success_target
        self.symbol = symbol

    def evaluate(self, range_object: dict[str: tuple[int, int]]) -> tuple[dict[str: tuple[int, int]], dict[str: tuple[int, int]]]:
        if self.key == "":
            raise ValueError(f"Range should not be checked for success_target={self.success_target}, {self.__repr__()}")

        fail_object = {key: value for key, value in range_object.items()}
        success_object = {key: value for key, value in range_object.items()}
        value_range = range_object[self.key]
        if self.symbol == "<":
            if value_range[0] > self.comparison_value:
                return fail_object, None
            elif value_range[1] <= self.comparison_value:
                return None, success_object
            elif value_range[0] < self.comparison_value:
                fail_object[self.key] = self.comparison_value, value_range[1]
                success_object[self.key] = value_range[0], self.comparison_value - 1
                return fail_object, success_object
        elif self.symbol == ">":
            if value_range[1] < self.comparison_value:
                return fail_object, None
            elif value_range[0] >= self.comparison_value:
                return None, success_object
            elif value_range[1] > self.comparison_value:
                fail_object[self.key] = value_range[0], self.comparison_value
                success_object[self.key] = self.comparison_value + 1, value_range[1]
                return fail_object, success_object
        else:
            raise ValueError(f"Range should not be checked for success_target={self.success_target}")

    def __repr__(self):
        return f"Instruction: key: {self.key}, comparison_value: {self.comparison_value}, method: {self.symbol}, success_target: {self.success_target}"


def not_in_list(accepted_range_objects: list[dict[str:int]], range_object: dict[str:int]):
    if len(accepted_range_objects) == 0:
        return True

    for accepted_range_object in accepted_range_objects:
        for key, value in accepted_range_object.items():
            if range_object[key] != value:
                return True

    return False


def process_range_objects() -> list[dict[str:tuple[int:int]]]:
    # tuple of range_objects and workflow to process next and the index of the corresponding instruction
    range_objects = [({"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}, "in", 0)]
    accepted_range_objects = []
    while len(range_objects) > 0:
        current_object, workflow_name, index = range_objects.pop(0)
        instructions = WORKFLOWS[workflow_name]

        instruction = instructions[index]
        if index == len(instructions) - 1:
            if instruction.success_target == "A":
                if not_in_list(accepted_range_objects, current_object):
                    accepted_range_objects.append(current_object)
            elif instruction.success_target != "R":
                range_objects.append((current_object, instruction.success_target, 0))
            continue

        fail, success = instruction.evaluate(current_object)
        if fail is not None:
            range_objects.append((fail, workflow_name, index + 1))

        if success is not None:
            if instruction.success_target == "A":
                if not_in_list(accepted_range_objects, current_object):
                    accepted_range_objects.append(current_object)
            elif instruction.success_target != "R":
                range_objects.append((success, instruction.success_target, 0))

    return accepted_range_objects


def find_distinct_combinations(all_object_ranges: list[dict[str:tuple[int, int]]]) -> int:
    number_of_combinations = 0
    for range_object in all_object_ranges:
        print(range_object)

    all_distinct_ranges = [all_object_ranges[0]]
    for index, range_object in enumerate(all_object_ranges):
        for comparison_index in range(index + 1, len(all_object_ranges)):
            comparison = all_object_ranges[comparison_index]
            # TODO find further distinct combinations

    for distinct_range in all_distinct_ranges:
        current_possibilities = (distinct_range["x"][1] - distinct_range["x"][0]) * (distinct_range["m"][1] - distinct_range["m"][0]) * (distinct_range["a"][1] - distinct_range["a"][0]) * (
                distinct_range["s"][1] - distinct_range["s"][0])
        print(current_possibilities, current_possibilities - 167_409_079_868_000, (current_possibilities - 167409079868000) / 167409079868000 * 100)
        print(distinct_range, current_possibilities)
        number_of_combinations += current_possibilities

    return number_of_combinations


for line in lines:
    if len(line) == 0:
        continue

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
                instructions.append(Instruction(match.group(1), int(match.group(3)), match.group(4), match.group(2)))

total_acceptance = 0
part_count = 0
all_object_ranges_accepted = process_range_objects()

combination_count = find_distinct_combinations(all_object_ranges_accepted)

print(combination_count, combination_count - 167409079868000, (combination_count - 167409079868000) / 167409079868000 * 100)
print(f"Total acceptance sum: {total_acceptance}. {part_count} were accepted")
