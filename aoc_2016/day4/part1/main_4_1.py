import aoc_2016.day4.common.rooms as rooms

valid_rooms = rooms.filter_real_rooms(rooms.read_rooms())
sum = 0
for room in valid_rooms:
    sum += room.section

print(sum)
