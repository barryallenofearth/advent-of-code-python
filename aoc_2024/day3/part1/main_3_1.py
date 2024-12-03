import re

MULTIPLICATION_PATTERN = re.compile(r"(mul\((\d+?),(\d+?)\))")

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"

result = 0
with open(file_name) as file:
    for line in file:
        line = line.strip()
        all_findings = MULTIPLICATION_PATTERN.findall(line)
        print(all_findings)

        for match, left, right in all_findings:
            print(match)
            result += int(left) * int(right)

print(f"The result is {result}")

# previous attempts
# 26366264 => too low
# 26186104
