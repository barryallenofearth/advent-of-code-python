import math
import re

import util.riddle_reader as riddle_reader
from util.strings import string_utils

lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)

number_of_configurations = 0
for index, line in enumerate(lines):
    line_possibilities = 0
    print(f"Evaluate line {index + 1}")
    split_line = line.split(" ")
    sequence = split_line[0]
    numbers = [int(number) for number in split_line[1].split(",")]
    expected_spring_count = sum(numbers)
    char_count = string_utils.count_chars_in_string(line)
    known_spring_count = char_count["#"] if '#' in char_count else 0
    if expected_spring_count == known_spring_count:
        line_possibilities = 1

    if line_possibilities == 0:
        regex = r"\.*" + ''.join([r"#{" + str(number) + r"}\." + ("+" if index < len(numbers) - 1 else "*") for index, number in enumerate(numbers)])
        print(regex)
        springs_pattern = re.compile(regex)
        question_mark_count = char_count["?"] if "?" in char_count else 0

        # represent all possible question mark values as binary number (either 1 or 0 <=> # or . and test all replacings
        highest_number = int(math.pow(2, question_mark_count))
        missing_number_of_springs = int(math.pow(2, expected_spring_count - known_spring_count)) - 1
        print(f"{highest_number} configurations are possible")
        for configuration_number in range(missing_number_of_springs, highest_number):
            replace_sequence = str(bin(configuration_number))[2:].rjust(question_mark_count, "0").replace("0", ".").replace("1", "#")
            if replace_sequence.count("#") + known_spring_count != expected_spring_count:
                continue

            current_sequence = sequence
            for symbol in replace_sequence:
                current_sequence = current_sequence.replace("?", symbol, 1)
            if springs_pattern.match(current_sequence):
                line_possibilities += 1

    number_of_configurations += line_possibilities
    print(f"Current number of possibilities: {line_possibilities}, total number: {number_of_configurations}")
