import re

DECOMPRESSION_PATTERN = r"\((\d+)x(\d+)\)[\w()]+"

with open("../riddle.txt") as file:
    for line in file:
        decompressed = ""
        line = line.strip()
        match_found = re.search(DECOMPRESSION_PATTERN, line)

        while bool(match_found):
            length = match_found.group(1)
            repetition_times = match_found.group(2)

            replace_pattern = r"\(" + length + "x" + repetition_times + "\)([\w()]{0," + length + "})"

            replace_matcher = re.search(pattern=replace_pattern, string=line)
            if bool(replace_matcher):
                repeated_string = replace_matcher.group(1)
                index_of_match = line.index(f"({length}x{repetition_times}){repeated_string}")
                before_pattern = line[:index_of_match]
                decompressed += before_pattern

                for time in range(0, int(repetition_times)):
                    decompressed += repeated_string

                line = re.sub(pattern=replace_pattern, repl="", string=line[index_of_match:], count=1)

            match_found = re.search(DECOMPRESSION_PATTERN, line)

        decompressed += line
        print(f"{decompressed}\n")

        print(f"The decompressed file is {len(decompressed)} symbols long.")
