import re

import util.riddle_reader as riddle_reader

SEEDS_TO_SOIL_MAP_START = "seed-to-soil map:"
SOIL_TO_FERTILIZER_MAP_START = "soil-to-fertilizer map:"
FERTILIZER_TO_WATER_MAP_START = "fertilizer-to-water map:"
WATER_TO_LIGHT_MAP_START = "water-to-light map:"
LIGHT_TO_TEMPERATURE_MAP_START = "light-to-temperature map:"
TEMPERATURE_TO_HUMIDITY_MAP_START = "temperature-to-humidity map:"
HUMIDITY_TO_LOCATION_MAP_START = "humidity-to-location map:"


class Mapping:

    def __init__(self, name: str, source_start_id: int, target_start_id: int, range: int):
        self.name = name
        self.source_start_id = source_start_id
        self.target_start_id = target_start_id
        self.target_stop_id = target_start_id + range - 1

    def __get_source_id(self, target_id: int) -> int:
        if self.target_start_id <= target_id <= self.target_stop_id:
            return self.source_start_id + (target_id - self.target_start_id)

        return -1

    def get_source_ids(self, target_id_range: tuple[int:int]) -> tuple[set[tuple[int::int]]:set[tuple[int::int]]]:
        mapped_ids = set()
        unmapped_ids = set()
        if target_id_range[1] < self.target_start_id or target_id_range[0] > self.target_stop_id:
            # completely outside of mapping range
            unmapped_ids.add(target_id_range)
        elif target_id_range[0] >= self.target_start_id and target_id_range[1] <= self.target_stop_id:
            # completely within range
            mapped_start_id = self.__get_source_id(target_id_range[0])
            mapped_stop_id = self.__get_source_id(target_id_range[1])
            mapped_ids.add((mapped_start_id, mapped_stop_id))
        elif target_id_range[0] < self.target_start_id and target_id_range[1] <= self.target_stop_id:
            # partially smaller, end within range

            mapped_start_id = target_id_range[0]
            mapped_stop_id = self.target_start_id - 1
            unmapped_ids.add((mapped_start_id, mapped_stop_id))

            mapped_start_id = self.__get_source_id(self.target_start_id)
            mapped_stop_id = self.__get_source_id(target_id_range[1])
            mapped_ids.add((mapped_start_id, mapped_stop_id))
        elif target_id_range[0] >= self.target_start_id and target_id_range[1] > self.target_stop_id:
            # partially larger, beginning within range
            mapped_start_id = self.__get_source_id(target_id_range[0])
            mapped_stop_id = self.__get_source_id(self.target_stop_id)
            mapped_ids.add((mapped_start_id, mapped_stop_id))

            mapped_start_id = self.target_stop_id + 1
            mapped_stop_id = target_id_range[1]
            unmapped_ids.add((mapped_start_id, mapped_stop_id))
        elif target_id_range[0] >= self.target_start_id and target_id_range[1] > self.target_stop_id:
            # beginning smaller, end larger than range
            mapped_start_id = target_id_range[0]
            mapped_stop_id = self.target_start_id - 1
            unmapped_ids.add((mapped_start_id, mapped_stop_id))

            mapped_start_id = self.__get_source_id(self.target_start_id)
            mapped_stop_id = self.__get_source_id(self.target_stop_id)
            mapped_ids.add((mapped_start_id, mapped_stop_id))

            mapped_start_id = self.target_stop_id + 1
            mapped_stop_id = target_id_range[1]
            unmapped_ids.add((mapped_start_id, mapped_stop_id))

        return mapped_ids, unmapped_ids

    def __repr__(self):
        return f"{self.name}: source_start_id={self.source_start_id}, target_range={self.target_start_id} to {self.target_stop_id}"


def map_id(target_id_list: set[tuple[int:int]], mappings: list[Mapping]) -> set[tuple[int:int]]:
    all_mapped_source_ids = set()

    all_unmapped_target_ids = set(target_id_list)
    for mapping in mappings:
        for _ in range(len(all_unmapped_target_ids)):
            current_range = all_unmapped_target_ids.pop()
            mapped_tuple_set, unmapped_tuple_set = mapping.get_source_ids(current_range)
            all_mapped_source_ids.update(mapped_tuple_set)
            all_unmapped_target_ids.update(unmapped_tuple_set)

    all_mapped_source_ids.update(all_unmapped_target_ids)
    return all_mapped_source_ids


def display_mappings(name: str, mappings: list[Mapping]):
    print(name)
    for mapping in mappings:
        print(mapping)


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

SEEDS_TO_SOIL = []
SOIL_TO_FERTILIZER = []
FERTILIZER_TO_WATER = []
WATER_TO_LIGHT = []
LIGHT_TO_TEMPERATURE = []
TEMPERATURE_TO_HUMIDITY = []
HUMIDITY_TO_LOCATION = []

currentMapList = SEEDS_TO_SOIL
currentName = ""
seeds = set()
for line in lines:
    if line.startswith("seeds:"):
        seed_strings = re.sub(r"seeds:\s+", "", lines[0].strip()).split(" ")
        for index in range(0, len(seed_strings), 2):
            starting_number = int(seed_strings[index])
            seed_id_range = int(seed_strings[index + 1])
            seeds.add((starting_number, starting_number + seed_id_range))
        print(f"seeds: {seeds}")
    elif line == SEEDS_TO_SOIL_MAP_START:
        currentMapList = SEEDS_TO_SOIL
        currentName = SEEDS_TO_SOIL_MAP_START
    elif line == SOIL_TO_FERTILIZER_MAP_START:
        currentMapList = SOIL_TO_FERTILIZER
        currentName = SOIL_TO_FERTILIZER_MAP_START
    elif line == FERTILIZER_TO_WATER_MAP_START:
        currentMapList = FERTILIZER_TO_WATER
        currentName = FERTILIZER_TO_WATER_MAP_START
    elif line == WATER_TO_LIGHT_MAP_START:
        currentMapList = WATER_TO_LIGHT
        currentName = WATER_TO_LIGHT_MAP_START
    elif line == LIGHT_TO_TEMPERATURE_MAP_START:
        currentMapList = LIGHT_TO_TEMPERATURE
        currentName = LIGHT_TO_TEMPERATURE_MAP_START
    elif line == TEMPERATURE_TO_HUMIDITY_MAP_START:
        currentMapList = TEMPERATURE_TO_HUMIDITY
        currentName = TEMPERATURE_TO_HUMIDITY_MAP_START
    elif line == HUMIDITY_TO_LOCATION_MAP_START:
        currentMapList = HUMIDITY_TO_LOCATION
        currentName = HUMIDITY_TO_LOCATION_MAP_START
    elif len(line) != 0:
        numbers = line.split(" ")
        currentMapList.append(Mapping(currentName, int(numbers[0]), int(numbers[1]), int(numbers[2])))

mimimum_location = 100000000000000
id_ranges = map_id(seeds, SEEDS_TO_SOIL)
id_ranges = map_id(id_ranges, SOIL_TO_FERTILIZER)
id_ranges = map_id(id_ranges, FERTILIZER_TO_WATER)
id_ranges = map_id(id_ranges, WATER_TO_LIGHT)
id_ranges = map_id(id_ranges, LIGHT_TO_TEMPERATURE)
id_ranges = map_id(id_ranges, TEMPERATURE_TO_HUMIDITY)
id_ranges = map_id(id_ranges, HUMIDITY_TO_LOCATION)
print(id_ranges)
for id_range in id_ranges:
    if id_range[0] < mimimum_location:
        mimimum_location = id_range[0]

print(f"The lowest location id is {mimimum_location}")
