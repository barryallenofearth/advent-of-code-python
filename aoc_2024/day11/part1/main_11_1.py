def main():
    TEST_MODE = False
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    with open(file_name, encoding="utf-8") as riddle_input:
        for line in riddle_input:
            stones = line.strip().split(" ")

        repetitions = 25
        for round in range(repetitions):
            print(f"Processing round {round}")
            new_sequence = []
            for stone in stones:
                if int(stone) == 0:
                    new_sequence.append("1")
                elif len(stone) % 2 == 0:
                    new_sequence.append(str(int(stone[:int(len(stone) / 2)])))
                    new_sequence.append(str(int(stone[int(len(stone) / 2):])))
                else:
                    new_sequence.append(f"{int(stone) * 2024}")
            stones = new_sequence
            print(f"After {repetitions} blinks {len(stones)} stones.")

        print(f"After {repetitions} blinks {len(stones)} stones.")


if __name__ == "__main__":
    main()
