import re

from util.strings import string_utils

TEST_MODE = False
file_name = "../"
if TEST_MODE:
    file_name += "test_riddle_1.txt"
else:
    file_name += "riddle.txt"

left = []
right = []
with open(file_name) as data:
    for line in data:
        split = re.split(r"\s+", line.strip())
        print(split)
        left.append(int(split[0]))
        right.append(split[1])

right_count = string_utils.count_chars_in_string(right)

total_sum = 0
for number_in_left in left:
    print(number_in_left)
    number_as_string = str(number_in_left)
    if number_as_string in right_count:
        total_sum += number_in_left * right_count[number_as_string]

print(f"The similarity score is {total_sum}")
