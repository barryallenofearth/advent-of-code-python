import math
import re

import util.riddle_reader as riddle_reader

CARD_ID_PATTERN = re.compile(r"^Card\s+(\d+):\s*")


def parse_number_list(number_list: str) -> list[int]:
    return [int(number) for number in re.split(r"\s+", number_list.strip())]


def card_score(winning_numbers: list[int], your_numbers: list[int]) -> int:
    match_count = 0
    for number in your_numbers:
        if number in winning_numbers:
            match_count += 1
    if match_count > 0:
        return int(math.pow(2, match_count - 1))
    else:
        return 0


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

total_score = 0
for line in lines:
    match = CARD_ID_PATTERN.search(line)
    card_id = int(match.group(1))
    line = line.replace(match.group(0), "").strip()
    number_blocks = line.split("|")
    winning_numbers = parse_number_list(number_blocks[0])
    your_numbers = parse_number_list(number_blocks[1])

    current_card_score = card_score(winning_numbers, your_numbers)
    total_score += current_card_score

    print(f"Card {card_id} score: {current_card_score}")

print(f"Total score {total_score}")
