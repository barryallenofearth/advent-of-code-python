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


def is_unsafe(numbers: list[int]) -> bool:
    print(f"Process sequence {numbers}")
    start_number = numbers[0]
    second_number = numbers[1]

    previous_number = start_number
    is_decreasing = second_number - start_number > 0
    for index in range(1, len(numbers)):
        current_number = numbers[index]
        difference = math.fabs(current_number - previous_number)
        if (is_decreasing and current_number <= previous_number) or (not is_decreasing and current_number >= previous_number):

            print(f"Increment direction wrong {line.strip()}: previous: {previous_number}, current: {current_number}")
            return True
        elif difference < MIN_STEP_SIZE or difference > MAX_STEP_SIZE:
            print(f"Step size wrong {line.strip()}: previous: {previous_number}, current: {current_number}")
            return True

        previous_number = current_number

    return False


with open(file_name) as file:
    for line in file:
        numbers = [int(value) for value in re.split(r"\s+", line.strip())]
        if not is_unsafe(numbers):
            print(f"This sequence is safe {line.strip()}")
            number_of_safe_modes += 1
            continue
        else:
            is_safe = False
            for index in range(len(numbers)):
                current_sequence = numbers[:]
                del current_sequence[index]
                if not is_unsafe(current_sequence):
                    print(f"This sequence is safe {line.strip()}")
                    number_of_safe_modes += 1
                    is_safe = True
                    break
            if not is_safe:
                print(f"This sequence is unsafe {line.strip()}")

print(f"The number of safe modes is {number_of_safe_modes}")
