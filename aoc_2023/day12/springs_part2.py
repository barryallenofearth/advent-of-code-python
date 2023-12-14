import math
import re

import util.riddle_reader as riddle_reader
from util.strings import string_utils

COMBINATOR_REPLACEMENTS = ["#", "."]


def is_matching_sequence(sequence: str, compiled_pattern, expected_spring_count: int) -> bool:
    if sequence.count("#") != expected_spring_count:
        return False

    return compiled_pattern.match(sequence)


lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)

number_of_configurations = 0
for index, line in enumerate(lines):
    line_possibilities = 0
    print(f"Evaluate line {index + 1}")
    split_line = line.split(" ")
    sequence = split_line[0]
    numbers = [int(number) for number in (','.join([split_line[1] for _ in range(5)])).split(",")]
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
        print(f"{highest_number} configurations are possible")
        possible_sequences = []
        for configuration_number in range(0, highest_number):
            binary_number = str(bin(configuration_number))[2:].rjust(question_mark_count, "0")
            replace_sequence = binary_number.replace("0", ".").replace("1", "#")

            possible_sequence = sequence
            for symbol in replace_sequence:
                possible_sequence = possible_sequence.replace("?", symbol, 1)

            minimum_number_of_springs_possible = possible_sequence.count("#") + known_spring_count * 5
            maximum_number_of_springs_possible = (possible_sequence.count("#") + known_spring_count) * 5 + 4

            if (maximum_number_of_springs_possible >= expected_spring_count) and minimum_number_of_springs_possible <= expected_spring_count:
                possible_sequences.append(possible_sequence)

        print(f"{len(possible_sequences)} sequences could lead to a matching pattern.")
        for sequence_index1, sequence1 in enumerate(possible_sequences):
            percentage = "{:5.2f}".format(sequence_index1 / len(possible_sequences) * 100)
            print(f"{percentage}% processed.")
            for combinator1 in COMBINATOR_REPLACEMENTS:
                for sequence2 in possible_sequences:
                    for combinator2 in COMBINATOR_REPLACEMENTS:

                        for sequence3 in possible_sequences:
                            for combinator3 in COMBINATOR_REPLACEMENTS:

                                for sequence4 in possible_sequences:
                                    for combinator4 in COMBINATOR_REPLACEMENTS:

                                        for sequence5 in possible_sequences:
                                            total_sequence = sequence1 + combinator1 + sequence2 + combinator2 + sequence3 + combinator3 + sequence4 + combinator4 + sequence5
                                            if is_matching_sequence(total_sequence, springs_pattern, expected_spring_count):
                                                line_possibilities += 1
    number_of_configurations += line_possibilities
    print(f"Current number of possibilities: {line_possibilities}, total number: {number_of_configurations}")
