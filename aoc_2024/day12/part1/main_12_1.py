from util.movement import coordinates
from util.movement.coordinates import Coordinates


def check_neighbor(coordinate: Coordinates, symbol: str, grid: dict[Coordinates:str], coordinates_checked: set[Coordinates], region_cells: set[Coordinates]):
    if coordinate in coordinates_checked or coordinate in region_cells:
        return

    previous_size = len(region_cells)
    region_cells.add(coordinate)
    while len(region_cells) > previous_size:
        previous_size = len(region_cells)
        matching_neighbors = coordinates.find_neighbors_of_symbol(coordinate, symbol, grid)
        for neighbor in matching_neighbors:
            check_neighbor(neighbor, symbol, grid, coordinates_checked, region_cells)


def check_coordinate(coordinate: Coordinates, symbol: str, grid: dict[Coordinates:str], coordinates_checked: set[Coordinates]) -> tuple[str, int, int]:
    if coordinate in coordinates_checked:
        return ()
    print(f"Check symbol {symbol} at {coordinate}")
    region_cells = set()
    check_neighbor(coordinate, symbol, grid, coordinates_checked, region_cells)

    inner_borders = len(region_cells) * 4
    # TODO calculate inner borders and multiply by two
    for cell in region_cells:
        inner_borders -= len(coordinates.find_neighbors_of_symbol(cell, symbol, grid))

    for region_cell in region_cells:
        coordinates_checked.add(region_cell)

    area_with_perimeter = (symbol, len(region_cells), inner_borders)

    return area_with_perimeter


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

        grid = coordinates.read_grid(lines, column_start=1, row_start=1)

        coordinates_checked = set()
        regions: list[tuple[str, int, int]] = []
        for coordinate, symbol in grid.items():
            regions.append(check_coordinate(coordinate, symbol, grid, coordinates_checked))

        total_price = 0
        for region in regions:
            if len(region) == 0:
                continue
            print(region)
            total_price += region[1] * region[2]

        print(f"The total price is {total_price}")


if __name__ == "__main__":
    main()
