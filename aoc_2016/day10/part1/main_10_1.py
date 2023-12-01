import re
from collections import defaultdict

from aoc_2016.day10.commons.instructions import BaseInstruction, HighLowInstruction, ValueToInstruction

HIGH_LOW_PATTERN = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
VALUE_TO_PATTERN = re.compile(r"value (\d+) goes to (bot|output) (\d+)")

bots = defaultdict(list)

outputs = defaultdict(list)


def is_bot_found() -> bool:
    for bot_id, bot_items in bots.copy().items():
        if len(bot_items) == 0:
            bots.pop(bot_id)

    for bot_id, bot_items in bots.items():
        if 61 in bot_items and 17 in bot_items:
            print(f"{bot_id} is the bot with the items {bot_items}")
            return True

    bot_with_2_items_exists = False
    for bot_id, bot_items in bots.items():
        if len(bot_items) == 2:
            bot_with_2_items_exists = True
            break

    if not bot_with_2_items_exists:
        print("No more bots with 2 items")

    print(f"bots: {bots}")
    print(f"outputs: {outputs}")
    
    return not bot_with_2_items_exists


def parse_instructions(path: str) -> list[BaseInstruction]:
    parsed_instructions = []
    with open(path) as file:
        for line in file:
            line = line.strip()
            high_low_pattern_match = HIGH_LOW_PATTERN.match(line)
            value_to_pattern_match = VALUE_TO_PATTERN.match(line)
            if bool(high_low_pattern_match):
                parsed_instructions.append(HighLowInstruction(high_low_pattern_match))
            elif bool(value_to_pattern_match):
                parsed_instructions.append(ValueToInstruction(value_to_pattern_match))

    return parsed_instructions


def handle_instructions(instructions: list[BaseInstruction]):
    while True:
        for instruction in instructions:
            if type(instruction) == HighLowInstruction:
                if len(bots[instruction.bot_id]) == 2:
                    instruction.handle_bot(bots, outputs)
            else:
                instruction.handle_bot(bots, outputs)

        if is_bot_found():
            break


# riddle_file = "../test_riddles.txt"
riddle_file = "../riddle.txt"
instructions = parse_instructions(riddle_file)
handle_instructions(instructions)

print(f"bots: {bots}")
print(f"outputs: {outputs}")

for bot_ids, bot_items in bots.items():
    if 61 in bot_items and 17 in bot_items:
        print(f"{bot_ids} is the bot with the items {bot_items}")
