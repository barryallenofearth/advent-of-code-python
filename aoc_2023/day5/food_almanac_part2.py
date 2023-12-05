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

    def get_source_id(self, target_id: int) -> int:
        if self.target_start_id <= target_id <= self.target_stop_id:
            return self.source_start_id + (target_id - self.target_start_id)

        return -1

    def __repr__(self):
        return f"{self.name}: source_start_id={self.source_start_id}, target_range={self.target_start_id} to {self.target_stop_id}"


def map_id(target_id: int, mappings: list[Mapping]):
    current_id = -1
    for mapping in mappings:
        mapped_id = mapping.get_source_id(target_id)
        if mapped_id > 0:
            current_id = mapped_id
            break
    if current_id < 0:
        current_id = target_id

    return current_id


def display_mappings(name: str, mappings: list[Mapping]):
    print(name)
    for mapping in mappings:
        print(mapping)


lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)

SEEDS_TO_SOIL = []
SOIL_TO_FERTILIZER = []
FERTILIZER_TO_WATER = []
WATER_TO_LIGHT = []
LIGHT_TO_TEMPERATURE = []
TEMPERATURE_TO_HUMIDITY = []
HUMIDITY_TO_LOCATION = []

currentMapList = SEEDS_TO_SOIL
currentName = ""
seeds = []
for line in lines:
    if line.startswith("seeds:"):
        seed_strings = re.sub(r"seeds:\s+", "", lines[0].strip()).split(" ")
        for index in range(0, len(seed_strings), 2):
            startingNumber = int(seed_strings[index])
            for seed in range(int(seed_strings[index + 1])):
                seeds.append(startingNumber + seed)
        print(f"seeds: {seeds}")
    elif line == SEEDS_TO_SOIL_MAP_START:
        currentMapList = SEEDS_TO_SOIL
        currentName = SEEDS_TO_SOIL_MAP_START
        display_mappings("seeds to soil:", SEEDS_TO_SOIL)
    elif line == SOIL_TO_FERTILIZER_MAP_START:
        currentMapList = SOIL_TO_FERTILIZER
        currentName = SOIL_TO_FERTILIZER_MAP_START
        display_mappings("soil to fertilizer:", SOIL_TO_FERTILIZER)
    elif line == FERTILIZER_TO_WATER_MAP_START:
        currentMapList = FERTILIZER_TO_WATER
        currentName = FERTILIZER_TO_WATER_MAP_START
        display_mappings("fertilizer to water:", FERTILIZER_TO_WATER)
    elif line == WATER_TO_LIGHT_MAP_START:
        currentMapList = WATER_TO_LIGHT
        currentName = WATER_TO_LIGHT_MAP_START
        display_mappings("water to light:", WATER_TO_LIGHT)
    elif line == LIGHT_TO_TEMPERATURE_MAP_START:
        currentMapList = LIGHT_TO_TEMPERATURE
        currentName = LIGHT_TO_TEMPERATURE_MAP_START
        display_mappings("light to temperature:", LIGHT_TO_TEMPERATURE)
    elif line == TEMPERATURE_TO_HUMIDITY_MAP_START:
        currentMapList = TEMPERATURE_TO_HUMIDITY
        currentName = TEMPERATURE_TO_HUMIDITY_MAP_START
        display_mappings("temperature to humidity:", TEMPERATURE_TO_HUMIDITY)
    elif line == HUMIDITY_TO_LOCATION_MAP_START:
        currentMapList = HUMIDITY_TO_LOCATION
        currentName = HUMIDITY_TO_LOCATION_MAP_START
        display_mappings("humidity to location:", HUMIDITY_TO_LOCATION)
    elif len(line) != 0:
        numbers = line.split(" ")
        currentMapList.append(Mapping(currentName, int(numbers[0]), int(numbers[1]), int(numbers[2])))










mapped_seeds_to_location = []
for seed in seeds:
    current_id = map_id(seed, SEEDS_TO_SOIL)
    current_id = map_id(current_id, SOIL_TO_FERTILIZER)
    current_id = map_id(current_id, FERTILIZER_TO_WATER)
    current_id = map_id(current_id, WATER_TO_LIGHT)
    current_id = map_id(current_id, LIGHT_TO_TEMPERATURE)
    current_id = map_id(current_id, TEMPERATURE_TO_HUMIDITY)
    current_id = map_id(current_id, HUMIDITY_TO_LOCATION)
    mapped_seeds_to_location.append(current_id)


print(f"The mapped location ids are: {mapped_seeds_to_location}")
mapped_seeds_to_location.sort()

print(f"The lowest location id is {mapped_seeds_to_location[0]}")
