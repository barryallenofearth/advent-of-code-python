import re

DECOMPRESSION_PATTERN = r"\((\d+)x(\d+)\)[\w()]+"


def replace_sequence(string: str) -> str:
    match_found = re.search(DECOMPRESSION_PATTERN, string)

    while bool(match_found):
        length = match_found.group(1)
        repetition_times = match_found.group(2)

        replace_pattern = r"\(" + length + "x" + repetition_times + "\)([\w()]{0," + length + "})"

        replace_matcher = re.search(pattern=replace_pattern, string=string)
        if bool(replace_matcher):
            originally_replaced_string = replace_matcher.group(1)

            replaced_string = replace_sequence(originally_replaced_string)
            decompressed_sequence = ""
            for time in range(0, int(repetition_times)):
                decompressed_sequence += replaced_string

            string = string.replace(f"({length}x{repetition_times}){originally_replaced_string}", decompressed_sequence, 1)

        match_found = re.search(DECOMPRESSION_PATTERN, string)

    return string


with open("../riddle.txt") as file:
    for line in file:
        line = line.strip()

        decompressed = replace_sequence(line)

        print(f"The decompressed file is {len(decompressed)} symbols long.")
