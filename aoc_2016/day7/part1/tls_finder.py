def filter_abba_ips():
    tls_ips = []
    with open("../riddle.txt") as file:
        for line in file:
            remaining_line = line.strip()

            if has_tls(remaining_line):
                print(line)
                tls_ips.append(line)

    return tls_ips


def has_tls(remaining_line):
    found_abba_sequence = False
    while len(remaining_line) != 0:

        try:
            closing_index = remaining_line.index("]")
        except ValueError:
            closing_index = -1

        if closing_index != -1:
            opening_index = remaining_line.index("[")
            if opening_index == 0:
                if contains_abba_sequence(remaining_line[1:closing_index]):
                    return False
                remaining_line = remaining_line[closing_index + 1:]
            else:
                if contains_abba_sequence(remaining_line[:opening_index]):
                    found_abba_sequence = True
                remaining_line = remaining_line[opening_index:]
        else:
            if contains_abba_sequence(remaining_line):
                found_abba_sequence = True
            break

    return found_abba_sequence


def contains_abba_sequence(sequence: str):
    for index in range(0, len(sequence) - 3):
        if sequence[index] != sequence[index + 1]:
            if sequence[index] == sequence[index + 3] and sequence[index + 1] == sequence[index + 2]:
                return True

    return False
