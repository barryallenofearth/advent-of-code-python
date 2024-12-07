import itertools
import multiprocessing
import re

TEST_MODE = False

LINE_PATTERN = re.compile(r"^(\d+): ((?:\d+ )+\d+)$")


class Equation:

    def __init__(self, result: int, terms: list[int]):
        self.result = result
        self.terms = terms


def read_riddle() -> list[Equation]:
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"

    equations = []

    with open(file_name) as file:
        for line in file:
            line = line.strip()
            line_match = LINE_PATTERN.match(line)
            if line_match:
                result = int(line_match.group(1))
                terms = [int(number) for number in line_match.group(2).split(" ")]
                equations.append(Equation(result, terms))
    return equations


def evaluate_equation(equation) -> int:
    all_combinations = itertools.product(['*', '+'], repeat=len(equation.terms) - 1)
    for current_combination in all_combinations:
        current_value = equation.terms[0]
        for index in range(len(current_combination)):
            if current_combination[index] == "+":
                current_value += equation.terms[index + 1]
            else:
                current_value *= equation.terms[index + 1]
        if equation.result == current_value:
            return equation.result

    return 0


def main():
    equations = read_riddle()

    pool = multiprocessing.Pool(1)
    total_result_sum = 0
    for equation in equations:
        validity_result = evaluate_equation(equation)
        print(equation.result, equation.terms, validity_result)
        total_result_sum += validity_result

    print(f"The total sum of all valid results is {total_result_sum}")


if __name__ == "__main__":
    main()
