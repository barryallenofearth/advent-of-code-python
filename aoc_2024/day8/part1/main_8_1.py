from util.movement import coordinates
from util.movement.coordinates import Coordinates


def main():
    TEST_MODE = False
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    with open(file_name, encoding="utf-8") as riddle_input:
        lines = []
        for line in riddle_input:
            line = line.strip()
            lines.append(line)

        grid = coordinates.read_grid(lines)
        coordinates.print_grid(grid)
        min_max_coordinates = coordinates.get_min_max_grid_coordinates(grid)
        antenna_locations = coordinates.find_symbols_in_grid(grid, ".", equals_check=False)

        frequencies = set()
        for antenna_location in antenna_locations:
            frequencies.add(grid[antenna_location])

        anti_nodes = set()
        for frequency in frequencies:
            frequency_locations = coordinates.find_symbols_in_grid(grid, frequency)

            for index in range(len(frequency_locations)):
                for comparison_index in range(len(frequency_locations)):

                    if index == comparison_index:
                        continue

                    location = frequency_locations[index]
                    comparison_location = frequency_locations[comparison_index]

                    vector = Coordinates(location.x - comparison_location.x, location.y - comparison_location.y)

                    location_anti_node_location = Coordinates(comparison_location.x - vector.x, comparison_location.y - vector.y)
                    if not coordinates.is_off_grid(location_anti_node_location, min_max_coordinates[0], min_max_coordinates[1]):
                        anti_nodes.add(location_anti_node_location)

                    comparison_anti_node_location = Coordinates(location.x + vector.x, location.y + vector.y)
                    if not coordinates.is_off_grid(comparison_anti_node_location, min_max_coordinates[0], min_max_coordinates[1]):
                        anti_nodes.add(comparison_anti_node_location)

        for anti_node in anti_nodes:
            grid[anti_node] = "#"

        coordinates.print_grid(grid)

        print(f"{len(anti_nodes)} unique locations were found")


if __name__ == "__main__":
    main()
