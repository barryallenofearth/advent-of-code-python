import util.riddle_reader as riddle_reader

line = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)[0]

sequences = line.split(",")
hash_code_sum = 0
for sequence in sequences:
    current_hash_code = 0
    for symbol in sequence:
        current_hash_code += ord(symbol)
        current_hash_code *= 17
        current_hash_code = current_hash_code % 256
    hash_code_sum += current_hash_code
    # print(f"current hash code for {sequence} is {current_hash_code}")


print(f"final hash code {hash_code_sum}")
