from util.movement.coordinates import Coordinates
import util.movement.facing as facing

with open("../riddle.txt") as riddle_input:
    commands = [command.strip() for command in riddle_input.read().split(",")]

print(commands)
coordinates = Coordinates(0, 0)
current_facing = facing.UP
visited_positions = [coordinates]


def go_steps_or_stop():
    global coordinates
    for step in range(number_of_steps):
        coordinates = facing.move_forward(coordinates, current_facing, 1)
        if coordinates in visited_positions:
            return False
        visited_positions.append(coordinates)
    return True


for command in commands:
    current_facing = facing.rotate(current_facing, command[0:1])
    number_of_steps = int(command[1:])
    if not go_steps_or_stop():
        break

print(f"The final coordinates are {coordinates}")
distance = abs(coordinates.x) + abs(coordinates.y)
print(distance)
