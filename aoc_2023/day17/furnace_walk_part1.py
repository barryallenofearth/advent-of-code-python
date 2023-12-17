from collections import defaultdict

import util.riddle_reader as riddle_reader
from util.movement import coordinates
from util.movement import facing
from util.movement.coordinates import Coordinates


class Path:

    def __init__(self, position: Coordinates, initial_facing: str, steps_taken_forward=0, total_heat_consumed=0, total_step_count=0):
        self.position = position
        self.facing = initial_facing
        self.steps_taken_forward = steps_taken_forward
        self.total_heat_consumed = total_heat_consumed
        self.total_step_count = total_step_count

    def __eq__(self, other):
        return (type(other) == type(self)
                and self.position == other.position
                and self.facing == other.facing
                and self.steps_taken_forward == other.steps_taken_forward
                and self.total_heat_consumed == other.total_heat_consumed
                and self.total_step_count == other.total_step_count)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return f"Path: position: {self.position}, facing: {self.facing}, steps_taken_forward: {self.steps_taken_forward}, total_heat_consumed: {self.total_heat_consumed}, total_step_count: {self.total_step_count}\n"


# keys tuple[coordinates, facing, steps_taken_forward)
PATH_MEMORY_MAP = defaultdict(lambda: 100000000000000000000000000)


# returns additional_paths and modifies
def set_further_options(current_path: Path, grid: dict[Coordinates, int], paths_to_follow: list[Path], min_coordinates: Coordinates, max_coordinates: Coordinates):
    def alter_path(path_to_alter: Path, next_position: Coordinates, next_facing: str):
        path_to_alter.position = next_position
        if path_to_alter.facing == next_facing:
            path_to_alter.steps_taken_forward += 1
        else:
            path_to_alter.steps_taken_forward = 0
        path_to_alter.facing = next_facing
        path_to_alter.total_step_count += 1
        path_to_alter.total_heat_consumed += grid[path_to_alter.position]

    next_positions = []
    if current_path.steps_taken_forward != 3:
        forward = facing.move_forward(current_path.position, current_path.facing, 1)
        if not coordinates.is_off_grid(forward, min_coordinates, max_coordinates):
            next_positions.append((forward, current_path.facing))

    left_rotation_facing = facing.rotate(current_path.facing, facing.ROTATE_LEFT)
    left_position = facing.move_forward(current_path.position, left_rotation_facing, 1)
    if not coordinates.is_off_grid(left_position, min_coordinates, max_coordinates):
        next_positions.append((left_position, left_rotation_facing))

    right_rotation_facing = facing.rotate(current_path.facing, facing.ROTATE_RIGHT)
    right_position = facing.move_forward(current_path.position, right_rotation_facing, 1)
    if not coordinates.is_off_grid(right_position, min_coordinates, max_coordinates):
        next_positions.append((right_position, right_rotation_facing))

    for index, next_position_with_facing in enumerate(next_positions):
        new_path = Path(Coordinates(current_path.position.x, current_path.position.y), current_path.facing,
                        current_path.steps_taken_forward, current_path.total_heat_consumed, current_path.total_step_count)
        alter_path(new_path, next_position_with_facing[0], next_position_with_facing[1])
        if add_if_no_better_value_is_known(paths_to_follow, new_path):
            if new_path.position.x == max_coordinates.x and new_path.position.y == max_coordinates.y:
                return new_path

    return None


def add_if_no_better_value_is_known(paths_to_follow: list[Path], path_to_add: Path) -> bool:
    global PATH_MEMORY_MAP
    history_tuple = (path_to_add.position, path_to_add.facing, path_to_add.steps_taken_forward)
    current_minimum_heat_loss = PATH_MEMORY_MAP[history_tuple]
    if path_to_add.total_heat_consumed < current_minimum_heat_loss:
        paths_to_follow.append(path_to_add)
        PATH_MEMORY_MAP[history_tuple] = path_to_add.total_heat_consumed
        return True
    else:
        return False


lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)
grid = coordinates.read_grid(lines, 1, 1)
for position, value in grid.items():
    grid[position] = int(value)

min_coordinates, max_coordinates = coordinates.print_grid(grid)

# random maximum assuming that every field has been visited 100 times and has a heat consumption of 9
paths_to_follow = [Path(Coordinates(min_coordinates.x, min_coordinates.y), facing.RIGHT), Path(Coordinates(min_coordinates.x, min_coordinates.y), facing.DOWN)]
for path in paths_to_follow:
    history_tuple = (path.position, path.facing, path.steps_taken_forward)
    PATH_MEMORY_MAP[history_tuple] = 0

step = 0
success_path = None
while len(paths_to_follow) != 0 and success_path is None:
    paths_to_follow.sort(key=lambda path: path.total_heat_consumed)
    step += 1
    current_path = paths_to_follow.pop(0)
    if current_path.position.x == max_coordinates.x and current_path.position.y == max_coordinates.y:
        success_path = current_path
        break

    if step % 10_000 == 0:
        print(step, len(paths_to_follow), current_path.total_heat_consumed, current_path.position)

    success_path = set_further_options(current_path, grid, paths_to_follow, min_coordinates, max_coordinates)

heat_loss_map = {}
for path in paths_to_follow[::-1]:
    heat_loss_map[path.position] = path.total_heat_consumed

coordinates.print_grid(heat_loss_map, min_coordinates, max_coordinates)

if success_path is not None:
    print(success_path.position)
    print(f"The minimum heat cost is {success_path.total_heat_consumed} in {success_path.total_step_count} at position {success_path.position}")
else:
    print(f"No result was found in {step} steps")
