import util.riddle_reader as riddle_reader
import util.strings.string_utils as string_utils


def card_value(card) -> int:
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    elif card == "T":
        return 10
    else:
        return int(card)


class HandOfCards:

    def __init__(self, original_hand: str, bid: int):
        self.bid = bid
        self.hand = self.__sort_hand(original_hand)
        self.type_value = self.get_type_value()
        self.card1 = card_value(original_hand[0])
        self.card2 = card_value(original_hand[1])
        self.card3 = card_value(original_hand[2])
        self.card4 = card_value(original_hand[3])
        self.card5 = card_value(original_hand[4])
        self.rank = 0

    @staticmethod
    def __sort_hand(hand: str) -> str:
        return "".join(sorted(hand, key=card_value, reverse=True))

    def get_type_value(self) -> int:
        list_of_counted_chars = string_utils.sort_counted_chars(string_utils.count_chars_in_string(self.hand), use_char_value_as_tie_breaker=False)
        if list_of_counted_chars[-1][1] == 5:
            return 6
        elif list_of_counted_chars[-1][1] == 4:
            return 5
        elif list_of_counted_chars[-1][1] == 3 and list_of_counted_chars[-2][1] == 2:
            return 4
        elif list_of_counted_chars[-1][1] == 3:
            return 3
        elif list_of_counted_chars[-1][1] == 2 and list_of_counted_chars[-2][1] == 2:
            return 2
        elif list_of_counted_chars[-1][1] == 2:
            return 1
        elif list_of_counted_chars[-1][1] == 1:
            return 0


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
hands_of_cards = []
for line in lines:
    split = line.split(" ")
    hands_of_cards.append(HandOfCards(split[0], int(split[1])))

hands_of_cards.sort(key=lambda hand: (hand.type_value, hand.card1, hand.card2, hand.card3, hand.card4, hand.card5))
total_score = 0
for rank in range(1, len(hands_of_cards) + 1):
    hand = hands_of_cards[rank - 1]
    current_score = rank * hand.bid
    print(rank, hand.hand, hand.bid, current_score)
    total_score += current_score

print(f"The total score is {total_score}")
