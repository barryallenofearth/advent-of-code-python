import re
from collections import defaultdict

import util.riddle_reader as riddle_reader

GAME_ID_PATTERN = re.compile(r"Game (\d+):")
COLOR_DRAWN_PATTERN = re.compile(r"(\d+) (red|green|blue)")

GREEN = "green"
RED = "red"
BLUE = "blue"

ALLOWED_MAXIMA = {RED: 12, GREEN: 13, BLUE: 14}

lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

id_sum = 0
for line in lines:
    id = int(GAME_ID_PATTERN.search(line).group(1))
    print(f"Process game {id}")
    line = line.replace(f"Game {id}: ", "")
    drawings = line.split(";")

    max_number_found = defaultdict(lambda: 0)
    for drawing in drawings:
        colors_drawn = drawing.strip().split(",")
        for color in colors_drawn:
            match = COLOR_DRAWN_PATTERN.match(color.strip())
            number = int(match.group(1))
            color = match.group(2)
            print(color, number)
            if number > max_number_found[color]:
                max_number_found[color] = number

    is_possilbe = True
    for color, max_number in max_number_found.items():
        is_possilbe = is_possilbe and ALLOWED_MAXIMA[color] >= max_number
        if not is_possilbe:
            print(f"Game is impossible: {color} appeared {max_number} times instead of {ALLOWED_MAXIMA[color]} times.")
            break

    if is_possilbe:
        id_sum += id
        print(f"Current id sum: {id_sum}")

print(f"Final id sum: {id_sum}")
