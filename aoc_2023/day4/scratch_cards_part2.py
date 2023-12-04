import math
import re

import util.riddle_reader as riddle_reader

CARD_ID_PATTERN = re.compile(r"^Card\s+(\d+):\s*")


class Card:

    def __init__(self, winning_numbers: str, your_numbers: str):
        self.winning_numbers = self.parse_number_list(winning_numbers)
        self.your_numbers = self.parse_number_list(your_numbers)
        self.card_score = self.calculate_card_score()
        self.cards_owned_of_this_type = 1

    @staticmethod
    def parse_number_list(number_list: str) -> list[int]:
        return [int(number) for number in re.split(r"\s+", number_list.strip())]

    def add_cards(self, number_of_cards):
        self.cards_owned_of_this_type += number_of_cards

    def calculate_card_score(self) -> int:
        match_count = 0
        for number in self.your_numbers:
            if number in self.winning_numbers:
                match_count += 1

        return match_count


def read_cards() -> tuple[list[int], dict[int:Card]]:
    lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

    ids = []
    cards = {}
    for line in lines:
        match = CARD_ID_PATTERN.search(line)
        card_id = int(match.group(1))
        ids.append(card_id)
        line = line.replace(match.group(0), "").strip()
        number_blocks = line.split("|")
        cards[card_id] = Card(number_blocks[0], number_blocks[1])

    return ids, cards


ordered_ids, cards = read_cards()

for card_id in ordered_ids:
    card = cards[card_id]
    for number in range(card_id + 1, card.card_score + card_id + 1):
        print(f"Add {card.cards_owned_of_this_type} of number {number}")
        cards[number].add_cards(card.cards_owned_of_this_type)

number_of_cards = 0
for card in cards.values():
    number_of_cards += card.cards_owned_of_this_type

print(f"You now own {number_of_cards} cards!")
