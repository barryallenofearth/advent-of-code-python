import re

BASE_PATH = "aoc_2023/day1/"
test = False
path = BASE_PATH
if test:
    path += "test2_riddle.txt"
else:
    path += "riddle.txt"

NUMBER_MAP = {"one": 1,
              "two": 2,
              "three": 3,
              "four": 4,
              "five": 5,
              "six": 6,
              "seven": 7,
              "eight": 8,
              "nine": 9}

pattern_or_group = "("
for key, value in NUMBER_MAP.items():
    pattern_or_group += key + "|"
pattern_or_group += "\d)"

pattern = r"^.*?" + pattern_or_group + ".*$"
print(f"forward pattern '{pattern}'")
NUMBER_PATTERN = re.compile(pattern)

pattern = r"^.*" + pattern_or_group + ".*?$"
print(f"reverse pattern '{pattern}'")
NUMBER_REVERSE_PATTERN = re.compile(pattern + ".*?")


def assembled_number(line: str) -> int:
    def get_number(found_string: str) -> int:
        if found_string in NUMBER_MAP:
            print(f"{found_string}: {NUMBER_MAP[found_string]}")
            return NUMBER_MAP[found_string]
        else:
            print(f"{found_string}: {found_string}")
            return int(found_string)

    found_string = NUMBER_PATTERN.match(line).group(1)
    found_reverse_string = NUMBER_REVERSE_PATTERN.match(line).group(1)
    sum = 10 * get_number(found_string) + get_number(found_reverse_string)
    print(f"new number {sum}")
    return sum


with open(path) as file:
    sum = 0
    index = 1
    for line in file:
        print("#", index, line)
        number = assembled_number(line.strip())
        sum += number
        print(f"current sum {sum}")
        index += 1

print(sum)
