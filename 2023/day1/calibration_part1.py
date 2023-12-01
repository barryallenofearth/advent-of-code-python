import re

test = False
if test:
    path = "test_"
else:
    path = "riddle.txt"


def get_first_int(line: str) -> int:
    for symbol in line:
        if re.match("^\d$", symbol):
            return int(symbol)


with open(path) as file:
    sum = 0
    for line in file:
        line = line.strip()
        sum += 10 * get_first_int(line)
        sum += get_first_int(line[::-1])

print(sum)
