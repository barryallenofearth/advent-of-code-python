import util.riddle_reader as riddle_reader

lines = riddle_reader.read_file(riddle_reader.TEST_RIDDLE_FILE)

for line in lines:
    split_line = line.split(" ")
    sequence = split_line[0]
    numbers = [int(number) for number in split_line[2].split(",")]

    number_index = 0
    current_sequence_length = 0
    for index, symbol in enumerate(sequence):
        if symbol == ".":
            continue

        if symbol == '#':
            current_sequence_length += 1

