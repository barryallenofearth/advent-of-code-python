from aoc_2016.day3.common import triangle

triangles = triangle.read_triangles()
print(f"{len(triangles)} triangles found")
valid_triangles = triangle.filter_valid_triangles(triangles)

print(f"{len(valid_triangles)} valid triangles found")
