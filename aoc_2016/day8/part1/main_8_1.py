import re

ROWS = 6
COLUMNS = 50

grid = [['.' for column in range(0, COLUMNS)] for row in range(0, ROWS)]


def print_grid():
    for row in grid:
        line = ""
        for entry in row:
            line += entry
        print(line)
    print()


def parse_instruction(instruction: str):
    print(instruction)
    matcher = re.match(r"rect (\d+)x(\d+)", instruction)
    if bool(matcher):
        return create_rectangle(int(matcher.group(2)), int(matcher.group(1)))

    matcher = re.match(r"rotate column x=(\d+) by (\d+)", instruction)
    if bool(matcher):
        return rotate_column(int(matcher.group(1)), int(matcher.group(2)))

    matcher = re.match(r"rotate row y=(\d+) by (\d+)", instruction)
    if bool(matcher):
        return rotate_row(int(matcher.group(1)), int(matcher.group(2)))


def create_rectangle(rows: int, columns: int):
    for column in range(0, columns):
        for row in range(0, rows):
            grid[row][column] = "#"


def rotate_column(column, rows_shift):
    original_column = [row[column] for row in grid]
    for row_index in range(0, ROWS):
        grid[(row_index + rows_shift) % ROWS][column] = original_column[row_index]


def rotate_row(row, column_shift):
    original_row = grid[row][:]
    for column_index in range(0, COLUMNS):
        grid[row][(column_index + column_shift) % COLUMNS] = original_row[column_index]


print_grid()
print()

with open("../riddle.txt") as file:
    for instruction in file:
        parse_instruction(instruction.strip())
        print_grid()

count = 0
for row in grid:
    for value in row:
        if value == '#':
            count += 1

print(f"{count} pixels are illuminated")
