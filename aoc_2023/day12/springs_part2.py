import math
import re

import util.riddle_reader as riddle_reader

lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)

number_of_configurations = 0
for index, line in enumerate(lines):
    line_possibilities = 0
    print(f"Evaluate line {index + 1}")
    split_line = line.split(" ")
    sequence = '?'.join([split_line[0] for _ in range(5)])
    number_strings = ','.join([split_line[1] for _ in range(5)])
    numbers = [int(number) for number in number_strings.split(",")]
    print(sequence, numbers)
    expected_spring_count = sum(numbers)
    known_spring_count = sequence.count("#")
    if expected_spring_count == known_spring_count:
        line_possibilities = 1

    if line_possibilities == 0:
        regex = r"\.*" + ''.join([r"#{" + str(number) + r"}\." + ("+" if index < len(numbers) - 1 else "*") for index, number in enumerate(numbers)])
        print(regex)
        springs_pattern = re.compile(regex)
        question_mark_count = sequence.count("?")

        # represent all possible question mark values as binary number (either 1 or 0 <=> # or . and test all replacings
        lowest_number = int(math.pow(2, expected_spring_count - known_spring_count)) - 1
        highest_number = int(math.pow(2, question_mark_count))
        print(f"{highest_number} configurations are possible, {lowest_number} configuration_number possible")
        for configuration_number in range(lowest_number, highest_number):
            percentage = configuration_number / highest_number * 100
            if configuration_number % int(highest_number / 100) == 0:
                percentage_string = "{:5.2f}".format(percentage)
                print(f"{percentage_string}% processed, current line possibilities found {line_possibilities}")
            binary_number = str(bin(configuration_number))[2:].rjust(question_mark_count, "0")
            replace_sequence = binary_number.replace("0", ".").replace("1", "#")
            if replace_sequence.count("#") + known_spring_count != expected_spring_count:
                continue

            current_sequence = sequence
            for symbol in replace_sequence:
                current_sequence = current_sequence.replace("?", symbol, 1)
            if springs_pattern.match(current_sequence):
                line_possibilities += 1

    number_of_configurations += line_possibilities
    print(f"Current number of possibilities: {line_possibilities}, total number: {number_of_configurations}")
