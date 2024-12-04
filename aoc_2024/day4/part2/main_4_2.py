from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"


def count_matching_xmas(x_coordinate: Coordinates, grid: dict[Coordinates:str]) -> bool:
    def get_left_to_top_right() -> str:
        letter_coordinates = facing.move_forward(x_coordinate, facing.RIGHT)
        letter_coordinates = facing.move_forward(letter_coordinates, facing.UP)
        print(letter_coordinates, grid[letter_coordinates])
        return grid[letter_coordinates]

    def get_left_to_top_left() -> str:
        letter_coordinates = facing.move_forward(x_coordinate, facing.UP)
        letter_coordinates = facing.move_forward(letter_coordinates, facing.LEFT)
        print(letter_coordinates, grid[letter_coordinates])
        return grid[letter_coordinates]

    def get_left_to_bottom_left() -> str:
        letter_coordinates = facing.move_forward(x_coordinate, facing.LEFT)
        letter_coordinates = facing.move_forward(letter_coordinates, facing.DOWN)
        print(letter_coordinates, grid[letter_coordinates])
        return grid[letter_coordinates]

    def get_left_to_bottom_right() -> str:
        letter_coordinates = facing.move_forward(x_coordinate, facing.DOWN)
        letter_coordinates = facing.move_forward(letter_coordinates, facing.RIGHT)
        print(letter_coordinates, grid[letter_coordinates])
        return grid[letter_coordinates]

    neighbour_letters = [get_left_to_top_right(), get_left_to_top_left(), get_left_to_bottom_left(), get_left_to_bottom_right()]
    m_count = 0
    s_count = 0
    for letter in neighbour_letters:
        if letter == "M":
            m_count += 1
        elif letter == "S":
            s_count += 1

    if m_count == 2 and s_count == 2:
        return True

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
