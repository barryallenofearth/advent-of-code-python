import re
from collections import defaultdict

import aoc_2023.util.riddle_reader as riddle_reader

GAME_ID_PATTERN = re.compile(r"Game (\d+):")
COLOR_DRAWN_PATTERN = re.compile(r"(\d+) (red|green|blue)")

GREEN = "green"
RED = "red"
BLUE = "blue"

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

power_sum = 0
for line in lines:
    id = int(GAME_ID_PATTERN.search(line).group(1))
    print(f"Process game {id}")
    line = line.replace(f"Game {id}: ", "")
    drawings = line.split(";")

    min_number_found = defaultdict(lambda: 0)
    for drawing in drawings:
        colors_drawn = drawing.strip().split(",")
        for color in colors_drawn:
            match = COLOR_DRAWN_PATTERN.match(color.strip())
            number = int(match.group(1))
            color = match.group(2)
            if min_number_found[color] < number:
                min_number_found[color] = number

    power = 0
    for color, number in min_number_found.items():
        if power == 0:
            power = number
        else:
            power *= number
    power_sum += power
    print(f"Current id sum: {power_sum}")

print(f"Final id sum: {power_sum}")
