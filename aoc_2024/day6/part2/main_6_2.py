import multiprocessing
from collections import defaultdict

from util.movement import coordinates, facing
from util.movement.coordinates import Coordinates

from joblib import Parallel, delayed

TEST_MODE = False
if TEST_MODE:
    file_name = "../test_riddle.txt"
else:
    file_name = "../riddle.txt"

with open(file_name) as file:
    lines = [line.strip() for line in file]

visited_spots = set()
grid = coordinates.read_grid(lines)
min_max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
initial_guard_postion = coordinates.find_symbols_in_grid(grid, "^")[0]
obstacle_positions = coordinates.find_symbols_in_grid(grid, "#")
visited_spots.add(initial_guard_postion)

guard_facing = facing.UP
positions_with_facings = defaultdict(set)
guard_position = initial_guard_postion
while True:
    positions_with_facings[guard_position].add(guard_facing)
    new_position = facing.move_forward(guard_position, guard_facing)
    if coordinates.is_off_grid(new_position, min_max_coordinates[0], min_max_coordinates[1]):
        break

    if new_position in obstacle_positions:
        guard_facing = facing.rotate(guard_facing, facing.ROTATE_RIGHT)
        continue

    guard_position = new_position
    visited_spots.add(guard_position)

obstacles_to_check = set()


def is_route_looped(obstacle_position: Coordinates) -> Coordinates:
    # print(f"Checking route for obstacle {obstacles_to_check.index(obstacle_position)}/{len(obstacles_to_check)}: {obstacle_position}")
    guard_position = initial_guard_postion
    guard_facing = facing.UP
    positions_with_facings = defaultdict(set)
    while True:
        positions_with_facings[guard_position].add(guard_facing)
        new_position = facing.move_forward(guard_position, guard_facing)

        if coordinates.is_off_grid(new_position, min_max_coordinates[0], min_max_coordinates[1]):
            return None

        if new_position in obstacle_positions or new_position == obstacle_position:
            guard_facing = facing.rotate(guard_facing, facing.ROTATE_RIGHT)
            continue

        guard_position = new_position
        visited_spots.add(guard_position)
        if guard_position in positions_with_facings and guard_facing in positions_with_facings[guard_position]:
            return obstacle_position


for position, facings in positions_with_facings.items():
    for current_facing in facings:
        new_obstacle = facing.move_forward(position, current_facing)
        if new_obstacle not in obstacle_positions:
            obstacles_to_check.add(new_obstacle)

obstacles_to_check = list(obstacles_to_check)
print(f"Check {len(obstacles_to_check)} possible obstacles.")
if __name__ == "__main__":
    pool = multiprocessing.Pool(32)
    new_obstacles = pool.map(is_route_looped, obstacles_to_check)
    new_obstacles = set(filter(lambda value: value is not None, new_obstacles))
    print(f"There {len(new_obstacles)} positions for a new obstacle, that lead to a guard being stuck in a loop")
