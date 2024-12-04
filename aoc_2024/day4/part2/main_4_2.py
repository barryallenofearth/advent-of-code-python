from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"


def count_matching_xmas(x_coordinate: Coordinates, grid: dict[Coordinates:str]) -> bool:
    def move_and_read(facings: tuple) -> str:
        letter_coordinates = x_coordinate
        for facing_value in facings:
            letter_coordinates = facing.move_forward(letter_coordinates, facing_value)

        return grid[letter_coordinates]

    top_left = move_and_read((facing.LEFT, facing.UP))
    top_right = move_and_read((facing.RIGHT, facing.UP))
    bottom_left = move_and_read((facing.LEFT, facing.DOWN))
    bottom_right = move_and_read((facing.RIGHT, facing.DOWN))

    if top_left == "M":
        if top_right == "M":
            return bottom_left == "S" and bottom_right == "S"
        elif bottom_left == "M":
            return top_right == "S" and bottom_right == "S"
    elif top_right == "M":
        if top_left == "M":
            return bottom_left == "S" and bottom_right == "S"
        elif bottom_right == "M":
            return top_left == "S" and bottom_left == "S"
    elif top_left == "S":
        if top_right == "S":
            return bottom_left == "M" and bottom_right == "M"
        elif bottom_left == "S":
            return top_right == "M" and bottom_right == "M"
    elif top_right == "S":
        if top_left == "S":
            return bottom_left == "M" and bottom_right == "M"
        elif bottom_right == "S":
            return top_left == "M" and bottom_left == "M"


    return False


total_xmas_count = 0
with open(file_name) as file:
    lines = [line.strip() for line in file]
    grid = coordinates.read_grid(lines)

    a_coordinates = coordinates.find_symbols_in_grid(grid, "A")

    min_max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
    for a_coordinate in a_coordinates:
        if a_coordinate.y == min_max_coordinates[0].y or a_coordinate.y == min_max_coordinates[1].y or a_coordinate.x == min_max_coordinates[0].x or a_coordinate.x == min_max_coordinates[1].x:
            continue
        print(a_coordinate)
        if count_matching_xmas(a_coordinate, grid):
            min_coordinates = facing.move_forward(a_coordinate, facing.LEFT, steps=2)
            min_coordinates = facing.move_forward(min_coordinates, facing.UP, steps=2)
            max_coordinates = facing.move_forward(a_coordinate, facing.RIGHT, steps=2)
            max_coordinates = facing.move_forward(max_coordinates, facing.DOWN, steps=2)
            coordinates.print_grid(grid, min_coordinates, max_coordinates)

            total_xmas_count += 1
            print(total_xmas_count)

print(f"The total number of xmas is {total_xmas_count}.")

# 2024 too high
