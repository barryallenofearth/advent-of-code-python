import re

from aoc_2016.day3.common.triangle import Triangle, filter_valid_triangles

triangles = []
with open("../riddle.txt") as file:
    for line in file:
        line = line.strip()
        sides = re.split(r'\s+', line)
        triangle = Triangle(int(sides[0]), int(sides[1]), int(sides[2]))
        triangles.append(triangle)

print(f"{len(triangles)} triangles found")
valid_triangles = filter_valid_triangles(triangles)

print(f"{len(valid_triangles)} valid triangles found")
