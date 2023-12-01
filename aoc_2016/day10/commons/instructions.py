from collections import defaultdict
from re import Match

BOT = "bot"


def add_item(item_to_bot: bool, receiver_id: int, item: int, bots: defaultdict[int:list], output: defaultdict[int:list]):
    if item_to_bot:
        receiver_bot = bots[receiver_id]
        if len(receiver_bot) > 0 and receiver_bot[0] > item:
            receiver_bot.insert(0, item)
        else:
            receiver_bot.append(item)

    else:
        output[receiver_id].append(item)


class BaseInstruction:

    # bot: Bot-ID belonging to bot with 2 microchips
    # bots: dictionary with Bot-ID as key and microchip values as list
    # output: dictionary with Output-ID as key and microchip values as list
    #
    # return: list of bots with 2 microchips after transaction
    def handle_bot(self, bots: defaultdict[int:list], output: defaultdict[int:list]):
        pass


class HighLowInstruction(BaseInstruction):

    def __init__(self, high_low_match: Match[str]):
        self.bot_id = int(high_low_match.group(1))
        self.low_to_bot = high_low_match.group(2) == BOT
        self.low_to_id = int(high_low_match.group(3))
        self.high_to_bot = high_low_match.group(4) == BOT
        self.high_to_id = int(high_low_match.group(5))

    def handle_bot(self, bots: defaultdict[int:list], output: defaultdict[int:list]):
        low_item = bots[self.bot_id][0]
        high_item = bots[self.bot_id][1]

        bots[self.bot_id].remove(low_item)
        bots[self.bot_id].remove(high_item)

        add_item(self.low_to_bot, self.low_to_id, low_item, bots, output)
        add_item(self.high_to_bot, self.high_to_id, high_item, bots, output)

    def __repr__(self):
        return (f"bot {self.bot_id} gives low to {'bot' if self.low_to_bot else 'output'} {self.low_to_id} "
                f"and high to {'bot' if self.high_to_bot else 'output'} {self.high_to_id}")


class ValueToInstruction(BaseInstruction):

    def __init__(self, value_to_match: Match[str]):
        self.item_value = int(value_to_match.group(1))
        self.bot_id = int(value_to_match.group(3))
        self.activated = False

    def handle_bot(self, bots: defaultdict[int:list], output: defaultdict[int:list]):
        if not self.activated:
            add_item(True, self.bot_id, self.item_value, bots, output)
            self.activated = True

    def __repr__(self):
        return f"value {self.item_value} goes to bot {self.bot_id}"
