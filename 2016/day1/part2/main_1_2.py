from util.movement.coordinates import Coordinates
import util.movement.facing as facing

with open("../riddle.txt") as riddle_input:
    commands = [command.strip() for command in riddle_input.read().split(",")]

print(commands)
coordinates = Coordinates(0, 0)
current_facing = facing.UP
visited_positions = [Coordinates(coordinates.x, coordinates.y)]


def go_steps_or_stop():
    for step in range(numberOfSteps):
        facing.move_forward(coordinates, current_facing, 1)
        for position in visited_positions:
            if position.x == coordinates.x and position.y == coordinates.y:
                return False
        visited_positions.append(Coordinates(coordinates.x, coordinates.y))
    return True


for command in commands:
    current_facing = facing.rotate(current_facing, command[0:1])
    numberOfSteps = int(command[1:])
    if not go_steps_or_stop():
        break

print(f"The final coordinates are {coordinates}")
distance = abs(coordinates.x) + abs(coordinates.y)
print(distance)
