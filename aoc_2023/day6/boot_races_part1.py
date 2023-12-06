import math
import re

import util.riddle_reader as riddle_reader


def get_numbers(line: str) -> list[int]:
    return [int(number) for number in re.split("\s+", line)[1:]]


def determine_number_of_winning_possibilities(race_duration: int, max_distance: int) -> int:
    def calculate_distance(time: int) -> int:
        return time * (race_duration - time)

    half_race_time = race_duration / 2
    lower_time_limit = math.ceil(half_race_time - math.sqrt(half_race_time * half_race_time - max_distance))
    upper_time_limit = int(half_race_time + math.sqrt(half_race_time * half_race_time - max_distance))

    lower_limit_distance = calculate_distance(lower_time_limit)
    upper_limit_distance = calculate_distance(upper_time_limit)

    # count without interval limits
    possibility_count = upper_time_limit - lower_time_limit - 1
    if lower_limit_distance > max_distance:
        possibility_count += 1
    if upper_limit_distance > max_distance:
        possibility_count += 1

    print(lower_time_limit, upper_time_limit, possibility_count)
    return possibility_count


lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)

times = get_numbers(lines[0])
distances = get_numbers(lines[1])

races = {times[index]: distances[index] for index in range(len(times))}

result = 1
for time, distance in races.items():
    print(f"race: time={time}, max_distance={distance}")
    result *= determine_number_of_winning_possibilities(time, distance)

print(f"The total result is {result}")
