from util.movement import coordinates, facing

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
guard_postion = coordinates.find_symbols_in_grid(grid, "^")[0]
obstacle_positions = coordinates.find_symbols_in_grid(grid, "#")
visited_spots.add(guard_postion)

guard_facing = facing.UP
while True:
    new_position = facing.move_forward(guard_postion, guard_facing)
    if coordinates.is_off_grid(new_position, min_max_coordinates[0], min_max_coordinates[1]):
        break

    if new_position in obstacle_positions:
        guard_facing = facing.rotate(guard_facing, facing.ROTATE_RIGHT)
        continue

    guard_postion = new_position
    visited_spots.add(guard_postion)

print(f"The guard visited {len(visited_spots)} spots")
