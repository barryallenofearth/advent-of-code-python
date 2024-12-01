import math
import re

import numpy as np

TEST_MODE = False
file_name = "../"
if TEST_MODE:
    file_name += "test_riddle.txt"
else:
    file_name += "riddle.txt"

left = []
right = []
with open(file_name) as data:
    for line in data:
        split = re.split(r"\s+", line.strip())
        print(split)
        left.append(int(split[0]))
        right.append(int(split[1]))

total_difference = 0
while len(left) != 0:
    left_min = np.min(left)
    right_min = np.min(right)

    total_difference += math.fabs(left_min - right_min)

    left.remove(left_min)
    right.remove(right_min)

print(f"The total difference is {total_difference}")
