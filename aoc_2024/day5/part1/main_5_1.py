import re

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"

ORDERING_PATTERN = re.compile(r"(\d+)\|(\d+)")
SEQUENCE_PATTERN = re.compile(r"^(?:\d+,)+\d+$")


class Comparison:

    def __init__(self, smaller: int, larger: int):
        self.smaller = smaller
        self.larger = larger


orderings: list[Comparison] = []
sequences: list[list[int]] = []

with open(file_name) as file:
    for line in file:
        line = line.strip()
        ordering_match = ORDERING_PATTERN.match(line)
        if ordering_match:
            orderings.append(Comparison(int(ordering_match.group(1)), int(ordering_match.group(2))))
            continue

        print(line)
        sequence_match = SEQUENCE_PATTERN.match(line)
        if sequence_match:
            sequences.append([int(value) for value in line.split(",")])

smaller_side = [comparison.smaller for comparison in orderings]
larger_side = [comparison.larger for comparison in orderings]

smallest_value = -1

for small_value in smaller_side:
    if small_value not in larger_side:
        smallest_value = small_value
        print(smallest_value)
        break

all_numbers = set()
for number in smaller_side:
    all_numbers.add(number)
for number in larger_side:
    all_numbers.add(number)

number_with_larger_values = {}
for number in all_numbers:
    number_with_larger_values[number] = [comparison.larger for comparison in filter(lambda comparison: comparison.smaller == number, orderings)]

total_number = 0
for sequence in sequences:
    invalid_sequence = False
    previous_number = sequence[0]
    for index in range(1, len(sequence)):
        if sequence[index] not in number_with_larger_values[previous_number]:
            # print(f"{sequence[index]} is not a number larger than {previous_number}")
            invalid_sequence = True

        previous_number = sequence[index]
    if invalid_sequence:
        print(f"Sequence {sequence} is invalid")
    else:
        print(f"Sequence {sequence} is valid")
        middle_number = sequence[int(len(sequence) / 2)]
        print(f"The middle number is {middle_number}")
        total_number += middle_number

print(f"Total number is {total_number}")