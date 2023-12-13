import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement.coordinates import Coordinates


def determine_lines_left_of_mirror_plane(grid: dict[Coordinates:str]) -> int:
    lines_left_of_mirror = 0

    min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
    for mirror_plane_row_index in range(2, max_coordinates.x + 1):
        error_count = 0
        for row in range(1, max_coordinates.x + 1):

            if mirror_plane_row_index - row < min_coordinates.x or mirror_plane_row_index + row - 1 > max_coordinates.x:
                break
            for column in range(1, max_coordinates.y + 1):
                position_left_of_mirror = Coordinates(mirror_plane_row_index - row, column)
                position_right_of_mirror = Coordinates(mirror_plane_row_index + row - 1, column)

                if grid[position_left_of_mirror] != grid[position_right_of_mirror]:
                    error_count += 1
                    if error_count > 1:
                        break

            if error_count > 1:
                break

        if error_count == 1:
            lines_left_of_mirror = mirror_plane_row_index - 1
            break

    return lines_left_of_mirror


def determine_lines_above_mirror_plane(grid: dict[Coordinates:str]) -> int:
    lines_above_mirror = 0

    min_coordinates, max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
    for mirror_plane_column_index in range(min_coordinates.y + 1, max_coordinates.y + 1):
        error_count = 0
        for column in range(min_coordinates.y, max_coordinates.y + 1):
            if mirror_plane_column_index - column < min_coordinates.y or mirror_plane_column_index + column - 1 > max_coordinates.y:
                break

            for row in range(min_coordinates.x, max_coordinates.x + 1):

                position_above_mirror = Coordinates(row, mirror_plane_column_index - column)
                position_below_mirror = Coordinates(row, mirror_plane_column_index + column - 1)

                if grid[position_above_mirror] != grid[position_below_mirror]:
                    error_count += 1
                    if error_count > 1:
                        break

            if error_count > 1:
                break

        if error_count == 1:
            lines_above_mirror = mirror_plane_column_index - 1
            break

    return lines_above_mirror


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

current_grid = []
grid_lines = [current_grid]
for line in lines:
    if line == "":
        current_grid = []
        grid_lines.append(current_grid)
    else:
        current_grid.append(line)

grids = [coordinates.read_grid(grid, 1, 1) for grid in grid_lines]

sum = 0
for index, grid in enumerate(grids):
    print(f"Evaluate grid {index + 1}")
    left_lines = determine_lines_left_of_mirror_plane(grid)
    if left_lines > 0:
        print(f"{left_lines} were found left of the mirror plane")
        sum += left_lines
    else:
        above_lines = determine_lines_above_mirror_plane(grid)
        print(f"{above_lines} were found above the mirror plane")
        sum += above_lines * 100

print(f"The sum of values is {sum}")
