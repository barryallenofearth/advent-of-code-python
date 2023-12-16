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


def process_beam(starting_position: Coordinates, start_facing: str, grid: dict[Coordinates:str], min_coordinates: Coordinates, max_coordinates: Coordinates) -> int:
    illumination_grid = defaultdict(list)
    beam_id = 1
    beams_to_process = [Beam(beam_id, starting_position, start_facing)]
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
    # illuminated_grid = grid
    for position, facings in illumination_grid.items():
        if len(facings) > 0:
            illuminated_tiles += 1
            # if grid[position] != ".":
            #     illuminated_grid[position] = grid[position]
            # elif len(facings) == 1:
            #     illuminated_grid[position] = facings[0]
            # else:
            #     illuminated_grid[position] = str(len(facings))

    # coordinates.print_grid(illuminated_grid)

    return illuminated_tiles


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
grid = coordinates.read_grid(lines, 1, 1)
coordinates.print_grid(grid)

min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)

max_tiles = 0
max_start_position = Coordinates(1, 1)
max_start_facing = facing.DOWN
for row in range(min_coordinates.x, max_coordinates.x + 1):
    starting_position = Coordinates(row, min_coordinates.y)
    starting_facing = facing.DOWN
    illuminated_tiles = process_beam(starting_position, starting_facing, grid, min_coordinates, max_coordinates)
    if illuminated_tiles > max_tiles:
        max_tiles = illuminated_tiles
        max_start_position = starting_position
        max_start_facing = starting_facing

for row in range(min_coordinates.x, max_coordinates.x + 1):
    starting_position = Coordinates(row, max_coordinates.y)
    starting_facing = facing.UP
    illuminated_tiles = process_beam(starting_position, starting_facing, grid, min_coordinates, max_coordinates)
    if illuminated_tiles > max_tiles:
        max_tiles = illuminated_tiles
        max_start_position = starting_position
        max_start_facing = starting_facing

for column in range(min_coordinates.y, max_coordinates.y + 1):
    starting_position = Coordinates(min_coordinates.x, column)
    starting_facing = facing.RIGHT
    illuminated_tiles = process_beam(starting_position, starting_facing, grid, min_coordinates, max_coordinates)
    if illuminated_tiles > max_tiles:
        max_tiles = illuminated_tiles
        max_start_position = starting_position
        max_start_facing = starting_facing

for column in range(min_coordinates.y, max_coordinates.y + 1):
    starting_position = Coordinates(max_coordinates.x, column)
    starting_facing = facing.LEFT
    illuminated_tiles = process_beam(starting_position, starting_facing, grid, min_coordinates, max_coordinates)
    if illuminated_tiles > max_tiles:
        max_tiles = illuminated_tiles
        max_start_position = starting_position
        max_start_facing = starting_facing

print(f"{max_tiles} is the maximum number of illuminated fields. starting at {max_start_position} with a facing {max_start_facing}")
