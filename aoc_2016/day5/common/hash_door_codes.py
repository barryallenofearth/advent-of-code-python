import hashlib as hash


def determine_matching_hash_codes(number_of_leading_zeros=5):

    with open("../riddle.txt") as file:
        door_id = file.read().strip()

    pass_code = ""
    index = 0

    print(door_id)
    expected_hex_start = "".join(["0" for number in range(number_of_leading_zeros)])
    while len(pass_code) < 8:
        value = bytes(f"{door_id}{index}", encoding="UTF-8")
        hash_value = hash.md5(value)
        hex_value = hash_value.hexdigest()

        if hex_value[:number_of_leading_zeros] == expected_hex_start:
            pass_code += hex_value[number_of_leading_zeros]
            print(f"{index}: {pass_code}")
        index += 1

    return pass_code
