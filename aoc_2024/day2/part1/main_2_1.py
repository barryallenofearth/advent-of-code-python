import math
import re

TEST_MODE = False

if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"

MIN_STEP_SIZE = 1
MAX_STEP_SIZE = 3

number_of_safe_modes = 0
with open(file_name) as file:
    for line in file:
        number_strings = re.split(r"\s+", line.strip())
        start_number = int(number_strings[0])
        second_number = int(number_strings[1])

        previous_number = start_number
        unsafe = False
        is_decreasing = second_number - start_number > 0
        for index in range(1, len(number_strings)):
            current_number = int(number_strings[index])
            if (is_decreasing and current_number <= previous_number) or (not is_decreasing and current_number >= previous_number):
                print(f"Increment direction wrong {line.strip()}: previous: {previous_number}, current: {current_number}")
                unsafe = True
                break
            difference = math.fabs(current_number - previous_number)
            if difference < MIN_STEP_SIZE or difference > MAX_STEP_SIZE:
                print(f"Step size wrong {line.strip()}: previous: {previous_number}, current: {current_number}")
                unsafe = True
                break
            previous_number = current_number

        if not unsafe:
            number_of_safe_modes += 1

print(f"The number of safe modes is {number_of_safe_modes}")
