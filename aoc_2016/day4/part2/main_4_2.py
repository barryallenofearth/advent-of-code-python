import aoc_2016.day4.common.rooms as rooms

valid_rooms = rooms.filter_real_rooms(rooms.read_rooms())

for room in valid_rooms:
    actual_name = ""
    for char in room.name:
        if char == '-':
            actual_name += " "
            continue
        actual_name += chr((ord(char) - ord('a') + room.section) % 26 + ord('a'))

    if actual_name == "northpole object storage":
        print("The northpole object storage section is " + str(room.section))

