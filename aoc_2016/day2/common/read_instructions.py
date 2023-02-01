from util.movement import facing


def read_file():
    all_steps = []
    with open("../riddle.txt") as file:
        lines = file.readlines()
        for row in lines:
            row_commands = []
            all_steps.append(row_commands)
            row = row.strip()
            for char in row:
                if char == "L":
                    char = facing.LEFT
                elif char == "R":
                    char = facing.RIGHT
                elif char == "U":
                    char = facing.UP
                elif char == "D":
                    char = facing.DOWN

                row_commands.append(char)
    return all_steps
