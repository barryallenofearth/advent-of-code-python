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


def is_unsafe(numbers: list[int], original_numbers: list[int], removed_current_number=False, removed_previous_number=False, last_attempt=False) -> bool:
    sequence_complete = False
    print(f"Process sequence {numbers}")
    start_number = numbers[0]
    second_number = numbers[1]

    previous_number = start_number
    is_decreasing = second_number - start_number > 0
    for index in range(1, len(numbers)):
        current_number = numbers[index]
        difference = math.fabs(current_number - previous_number)
        if (is_decreasing and current_number <= previous_number) or (not is_decreasing and current_number >= previous_number):
            numbers = original_numbers[:]

            print(f"Increment direction wrong {line.strip()}: previous: {previous_number}, current: {current_number} => " + (
                "don't " if (removed_previous_number or removed_current_number) else "") + "tolerate")
            if not removed_previous_number:
                print(f"Remove previous number: {numbers[index - 1]}")
                removed_previous_number = True
                del numbers[index - 1]
            elif not removed_current_number:
                print(f"Remove current number: {numbers[index + 1]}")
                removed_current_number = True
                del numbers[index + 1]

            break
        elif difference < MIN_STEP_SIZE or difference > MAX_STEP_SIZE:
            numbers = original_numbers[:]

            print(f"Step size wrong {line.strip()}: previous: {previous_number}, current: {current_number} => " + (
                "don't " if (removed_previous_number or removed_current_number) else "") + "tolerate")
            if not removed_previous_number:
                removed_previous_number = True
                print(f"Remove previous number: {numbers[index - 1]}")
                del numbers[index - 1]
            elif not removed_current_number:
                removed_current_number = True
                print(f"Remove current number: {numbers[index + 1]}")
                del numbers[index + 1]
            break
        elif index == len(numbers) - 1:
            sequence_complete = True
        previous_number = current_number

    if not sequence_complete:
        if not last_attempt:
            return is_unsafe(numbers, original_numbers, removed_current_number, removed_previous_number, removed_previous_number and removed_current_number)
        else:
            return True
    return False


with open(file_name) as file:
    for line in file:
        numbers = [int(value) for value in re.split(r"\s+", line.strip())]

        if not is_unsafe(numbers, numbers, False, False):
            print(f"This sequence is safe {line.strip()}")
            number_of_safe_modes += 1
        else:
            print(f"This sequence is unsafe {line.strip()}")

print(f"The number of safe modes is {number_of_safe_modes}")
