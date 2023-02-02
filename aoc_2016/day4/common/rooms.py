import re
from util.strings import string_utils


class Room:

    def __init__(self, name: str, section: str, checksum: str):
        self.name = name
        self.section = section
        self.checksum = checksum

    def __str__(self):
        return f"(name={self.name},section={self.section},checksum={self.checksum}"


def read_rooms():
    all_rooms = []
    with open("../riddle.txt") as file:
        for room in file:
            room = room.strip()

            last_dash_index = len(room) - 1 - room.strip()[::-1].index("-")
            name = room[: last_dash_index]
            section = int(room[last_dash_index + 1: room.index("[")])
            checksum = room[room.index("[") + 1:room.index("]")]
            all_rooms.append(Room(name, section, checksum))

    return all_rooms


def filter_real_rooms(all_rooms: list):
    valid_rooms = []

    for room in all_rooms:
        only_letters = re.findall(string=room.name, pattern=r"\w")
        name = "".join(only_letters)

        char_encounter = string_utils.count_chars_in_string(name)
        items = string_utils.sort_counted_chars(char_encounter)
        sorted_list = [entry[0] for entry in items]
        expected_checksum = "".join(sorted_list[:5])
        if expected_checksum == room.checksum:
            valid_rooms.append(room)

    return valid_rooms
