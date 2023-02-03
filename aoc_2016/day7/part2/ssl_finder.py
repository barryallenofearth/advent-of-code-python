def find_ssl_ips():
    with open("../riddle.txt") as file:
        ip_addresses = file.readlines()

    ssl_addresses = []
    for address in ip_addresses:
        split = address.strip().split("[")
        outside_brackets = [part for part in split if "]" not in part]
        inside_brackets = []
        for part in split:
            if "]" in part:
                part_split = part.split("]")
                inside_brackets.append(part_split[0])
                outside_brackets.append(part_split[1])

        bab_sequences = []
        for outside in outside_brackets:
            for index in range(0, len(outside) - 2):
                a = outside[index]
                b = outside[index + 1]
                if a == outside[index + 2] and a != b:
                    bab_sequences.append(b + a + b)

        if contains_bab_sequence(inside_brackets, bab_sequences):
            ssl_addresses.append(address)

    return ssl_addresses


def contains_bab_sequence(inside_brackets: list, bab_sequences: list):
    for inside_bracket in inside_brackets:
        for bab in bab_sequences:
            if bab in inside_bracket:
                return True
