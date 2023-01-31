from util.movement.coordinates import Coordinates

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"

ROTATE_RIGHT = "R"
ROTATE_LEFT = "L"

'''The coordinate system is assumed to be from top y=0 to increasing values while moving down. 
Left and Right are handled as expected'''


def move_forward(position: Coordinates, facing: str, steps: int):
    if facing == UP:
        position.y = position.y - steps
    elif facing == RIGHT:
        position.x = position.x + steps
    elif facing == DOWN:
        position.y = position.y + steps
    elif facing == LEFT:
        position.x = position.x - steps
    else:
        raise ValueError(f"'{facing}' is not a valid facing")


def rotate(current_facing: str, rotation: str):
    if rotation != ROTATE_LEFT and rotation != ROTATE_RIGHT:
        raise ValueError(f"'{rotation}' is not a valid rotation")

    if current_facing == UP:
        if rotation == ROTATE_RIGHT:
            return RIGHT
        elif rotation == ROTATE_LEFT:
            return LEFT

    elif current_facing == RIGHT:
        if rotation == ROTATE_RIGHT:
            return DOWN
        elif rotation == ROTATE_LEFT:
            return UP

    elif current_facing == DOWN:
        if rotation == ROTATE_RIGHT:
            return LEFT
        elif rotation == ROTATE_LEFT:
            return RIGHT

    elif current_facing == LEFT:
        if rotation == ROTATE_RIGHT:
            return UP
        elif rotation == ROTATE_LEFT:
            return DOWN
    else:
        raise ValueError(f"'{current_facing}' is not a valid facing")
