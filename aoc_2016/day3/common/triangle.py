import re


class Triangle:

    def __init__(self, side_a, side_b, side_c):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def __str__(self):
        return f"({self.side_a},{self.side_b},{self.side_c})"


def filter_valid_triangles(triangles: list):
    return [triangle for triangle in triangles if triangle.side_a + triangle.side_b > triangle.side_c
            and triangle.side_a + triangle.side_c > triangle.side_b
            and triangle.side_b + triangle.side_c > triangle.side_a]
