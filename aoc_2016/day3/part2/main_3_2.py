import re

from aoc_2016.day3.common.triangle import Triangle, filter_valid_triangles

triangles = []
with open("../riddle.txt") as file:
    lines = file.readlines()
    for index in range(0, len(lines), 3):
        line1 = lines[index].strip()
        line2 = lines[index + 1].strip()
        line3 = lines[index + 2].strip()
        sides1 = re.split(r'\s+', line1)
        sides2 = re.split(r'\s+', line2)
        sides3 = re.split(r'\s+', line3)
        for triangle in range(0, 3):
            t = Triangle(int(sides1[triangle]), int(sides2[triangle]), int(sides3[triangle]))
            triangles.append(t)

print(f"{len(triangles)} triangles found")
valid_triangles = filter_valid_triangles(triangles)

print(f"{len(valid_triangles)} valid triangles found")
