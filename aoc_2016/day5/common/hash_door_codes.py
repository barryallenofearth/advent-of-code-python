import hashlib as hash
import re


def determine_matching_hash_codes(number_of_leading_zeros=5, is_position_mode=False):
    with open("../riddle.txt") as file:
        door_id = file.read().strip()

    if is_position_mode:
        pass_code = "________"
    else:
        pass_code = ""

    index = 0
    print(door_id)

    expected_hex_start = "".join(["0" for number in range(number_of_leading_zeros)])
    while len(pass_code) < 8 or "_" in pass_code:
        value = bytes(f"{door_id}{index}", encoding="UTF-8")
        hash_value = hash.md5(value)
        hex_value = hash_value.hexdigest()

        if hex_value[:number_of_leading_zeros] == expected_hex_start:
            if is_position_mode:
                if re.match(pattern="\d", string=hex_value[number_of_leading_zeros]) and int(hex_value[number_of_leading_zeros]) <= 7 and pass_code[int(hex_value[number_of_leading_zeros])] == "_":
                    print(hex_value)
                    pass_code_index = int(hex_value[number_of_leading_zeros])
                    pass_code = pass_code[:pass_code_index] + hex_value[number_of_leading_zeros + 1] + pass_code[pass_code_index + 1:]
            else:
                pass_code += hex_value[number_of_leading_zeros]
            print(f"{index}: {pass_code}")

        index += 1
        if index % 1000000 == 0:
            print(index)

    return pass_code
