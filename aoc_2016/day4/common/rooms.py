import re


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
            print(all_rooms[-1])

    return all_rooms


def filter_real_rooms(all_rooms: list):
    valid_rooms = []

    for room in all_rooms:
        char_encounter = {}
        findall = re.findall(string=room.name, pattern=r"\w")
        name = "".join(findall)
        for char in name:
            char_encounter[char] = 0
            for reference_char in name:
                if char == reference_char:
                    char_encounter[char] = char_encounter[char] + 1

        items = [item for item in char_encounter.items()]
        items.sort(key=lambda x: (-x[1], x[0]))
        sorted_list = [entry[0] for entry in items]
        expected_checksum = "".join(sorted_list[:5])
        if expected_checksum == room.checksum:
            valid_rooms.append(room)

    return valid_rooms
