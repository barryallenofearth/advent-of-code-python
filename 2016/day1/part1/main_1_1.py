from util.movement.coordinates import Coordinates
import util.movement.facing as facing

with open("../riddle.txt") as riddle_input:
    commands = [command.strip() for command in riddle_input.read().split(",")]

print(commands)
coordinates = Coordinates(0, 0)
current_facing = facing.UP
for command in commands:
    current_facing = facing.rotate(current_facing, command[0:1])
    facing.move_forward(coordinates, current_facing, int(command[1:]))
    print(f"{current_facing} {coordinates}")

distance = abs(coordinates.x) + abs(coordinates.y)
print(distance)
