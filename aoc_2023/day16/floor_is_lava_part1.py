from collections import defaultdict

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates


class Beam:

    def __init__(self, beam_id: int, initial_position: Coordinates, initial_facing: str):
        self.beam_id = beam_id
        self.position = initial_position
        self.facing = initial_facing


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
grid = coordinates.read_grid(lines, 1, 1)
coordinates.print_grid(grid)
# keys: coordinates and facing, values: list of beam ids
illumination_grid = defaultdict(list)

beam_id = 1
beams_to_process = [Beam(beam_id, Coordinates(1, 1), facing.RIGHT)]

min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)

while len(beams_to_process) > 0:
    beam = beams_to_process.pop(0)
    while True:
        if beam.facing in illumination_grid[beam.position]:
            # this field has already seen a beam with this facing => no new illuminated fields will follow
            break

        illumination_grid[beam.position].append(beam.facing)

        if grid[beam.position] == "/":
            if beam.facing == facing.UP:
                beam.facing = facing.RIGHT
            elif beam.facing == facing.RIGHT:
                beam.facing = facing.UP
            elif beam.facing == facing.LEFT:
                beam.facing = facing.DOWN
            elif beam.facing == facing.DOWN:
                beam.facing = facing.LEFT
        elif grid[beam.position] == "\\":
            if beam.facing == facing.UP:
                beam.facing = facing.LEFT
            elif beam.facing == facing.LEFT:
                beam.facing = facing.UP
            elif beam.facing == facing.RIGHT:
                beam.facing = facing.DOWN
            elif beam.facing == facing.DOWN:
                beam.facing = facing.RIGHT
        elif grid[beam.position] == "-":
            if beam.facing == facing.UP or beam.facing == facing.DOWN:
                beam.facing = facing.LEFT
                beam_id += 1
                beams_to_process.append(Beam(beam_id, Coordinates(beam.position.x, beam.position.y), facing.RIGHT))
        elif grid[beam.position] == "|":
            if beam.facing == facing.LEFT or beam.facing == facing.RIGHT:
                beam.facing = facing.UP
                beam_id += 1
                beams_to_process.append(Beam(beam_id, Coordinates(beam.position.x, beam.position.y), facing.DOWN))
        next_position = facing.move_forward(beam.position, beam.facing, 1)
        if min_coordinates.x <= next_position.x <= max_coordinates.x and min_coordinates.y <= next_position.y <= max_coordinates.y:
            beam.position = next_position

illuminated_tiles = 0
illuminated_grid = grid
for position, facings in illumination_grid.items():
    if len(facings) > 0:
        illuminated_tiles += 1
        if grid[position] != ".":
            illuminated_grid[position] = grid[position]
        elif len(facings) == 1:
            illuminated_grid[position] = facings[0]
        else:
            illuminated_grid[position] = str(len(facings))

coordinates.print_grid(illuminated_grid)

print(f"{illuminated_tiles} fields are illuminated")
