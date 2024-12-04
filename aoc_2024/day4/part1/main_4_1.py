from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"

FURTHER_LETTERS = ["M", "A", "S"]


def count_matching_xmas(x_coordinate: Coordinates, grid: dict[Coordinates:str], min_max_coordinates: tuple[Coordinates, Coordinates]) -> int:
    def is_letter(letter_coordinate: Coordinates, letter: str) -> bool:
        if coordinates.is_off_grid(letter_coordinate, min_max_coordinates[0], min_max_coordinates[1]):
            print(f"{letter_coordinate} is off grid")
            return False
        if grid[letter_coordinate] != letter:
            print(f"actual letter: {grid[letter_coordinate]}")
            return False
        return True

    def check_left_to_right() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.RIGHT)
            if not is_letter(letter_coordinates, letter):
                print("right", letter_coordinates, letter)
                return False
        return True

    def check_left_to_top_right() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.RIGHT)
            letter_coordinates = facing.move_forward(letter_coordinates, facing.UP)
            if not is_letter(letter_coordinates, letter):
                print("top right:", letter_coordinates, letter)
                return False
        return True

    def check_left_to_top() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.UP)
            if not is_letter(letter_coordinates, letter):
                print("top", letter_coordinates, letter)
                return False
        return True

    def check_left_to_top_left() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.UP)
            letter_coordinates = facing.move_forward(letter_coordinates, facing.LEFT)
            if not is_letter(letter_coordinates, letter):
                print("top_left:", letter_coordinates, letter)
                return False
        return True

    def check_left_to_left() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.LEFT)
            if not is_letter(letter_coordinates, letter):
                print("left:", letter_coordinates, letter)
                return False
        return True

    def check_left_to_bottom_left() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.LEFT)
            letter_coordinates = facing.move_forward(letter_coordinates, facing.DOWN)
            if not is_letter(letter_coordinates, letter):
                print("bottom_left:", letter_coordinates, letter)
                return False
        return True

    def check_left_to_bottom() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.DOWN)
            if not is_letter(letter_coordinates, letter):
                print("bottom:", letter_coordinates, letter)
                return False
        return True

    def check_left_to_bottom_right() -> bool:
        letter_coordinates = x_coordinate
        for letter in FURTHER_LETTERS:
            letter_coordinates = facing.move_forward(letter_coordinates, facing.DOWN)
            letter_coordinates = facing.move_forward(letter_coordinates, facing.RIGHT)
            if not is_letter(letter_coordinates, letter):
                print("bottom_right:", letter_coordinates, letter)
                return False
        return True

    count = 0

    if check_left_to_right():
        count += 1
    if check_left_to_top_right():
        count += 1
    if check_left_to_top():
        count += 1
    if check_left_to_top_left():
        count += 1
    if check_left_to_left():
        count += 1
    if check_left_to_bottom_left():
        count += 1
    if check_left_to_bottom():
        count += 1
    if check_left_to_bottom_right():
        count += 1

    return count


total_xmas_count = 0
with open(file_name) as file:
    lines = [line.strip() for line in file]
    grid = coordinates.read_grid(lines)

    x_coordinates = coordinates.find_symbols_in_grid(grid, "X")

    min_max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
    for x_coordinate in x_coordinates:
        print(x_coordinate)
        total_xmas_count += count_matching_xmas(x_coordinate, grid, min_max_coordinates)

print(f"The total number of xmas is {total_xmas_count}.")
