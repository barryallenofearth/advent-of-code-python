import re

import util.riddle_reader as riddle_reader


def determine_next_number(sequences: list[list[int]]):
    def are_all_zeros(sequence: list[int]):
        for number in sequence:
            if number != 0:
                return False
        return True

    differences = []
    for index in range(len(sequences[-1]) - 1):
        differences.append(sequences[-1][index + 1] - sequences[-1][index])

    sequences.append(differences)

    if not are_all_zeros(differences):
        return determine_next_number(sequences)

    current_last_number = 0
    for sequence_index in range(len(sequences) - 1, 0, -1):
        last_number_in_sequence = sequences[sequence_index][-1]
        last_number_in_previous_sequence = sequences[sequence_index - 1][-1]
        current_last_number = last_number_in_sequence + last_number_in_previous_sequence
        sequences[sequence_index - 1].append(current_last_number)

    return current_last_number


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

sum = 0
for line in lines:
    numbers = [int(string) for string in line.split(" ")]
    next_number = determine_next_number([numbers])
    sum += next_number
    print(f"The next number is {next_number}")

print(f"The sum of numbers is {sum}")
