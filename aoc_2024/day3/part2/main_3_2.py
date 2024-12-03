import re

MULTIPLICATION_PATTERN = re.compile(r"(do\(\)|don't\(\)|mul\((\d+?),(\d+?)\))")

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle_2.txt"
else:
    file_name = "../riddle.txt"

multiplication_enabled = True
result = 0
with open(file_name) as file:
    for line in file:
        line = line.strip()
        all_findings = MULTIPLICATION_PATTERN.findall(line)
        print(all_findings)

        for finding in all_findings:
            print(finding)
            if finding[0] == "do()":
                multiplication_enabled = True
            elif finding[0] == "don't()":
                multiplication_enabled = False
            elif multiplication_enabled:
                result += int(finding[1]) * int(finding[2])

print(f"The result is {result}")

# previous attempts
# 26366264 => too low
# 26186104
