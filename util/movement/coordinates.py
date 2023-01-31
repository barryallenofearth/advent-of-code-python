class Coordinates:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return type(other) == type(self) and self.x == other.x and self.y == other.y
