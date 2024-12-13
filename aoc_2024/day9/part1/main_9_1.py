import re


def main():
    def find_first_free_slot(file_allocation_sequence: list):
        for index in range(len(file_allocation_sequence)):
            if file_allocation_sequence[index] == ".":
                return index

        return -1

    def find_last_number(file_allocation_sequence: list):
        for index in range(len(file_allocation_sequence) - 1, 0, -1):
            if file_allocation_sequence[index] != ".":
                return index

        return -1

    TEST_MODE = False
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    file_allocation = []
    with open(file_name, encoding="utf-8") as riddle_input:
        for line in riddle_input:
            line = line.strip()

        for index in range(len(line)):
            number = int(line[index])
            if index % 2 == 0:
                file_index = int(index / 2)
                for _ in range(number):
                    file_allocation.append(f"{file_index}")
            else:
                for _ in range(number):
                    file_allocation.append(".")

    resorted = "".join(file_allocation)
    print(resorted)
    sorting_complete = re.compile(r"^\d+\.+$")
    while not sorting_complete.match(resorted):
        first_free_slot = find_first_free_slot(file_allocation)

        last_position_of_last_number = find_last_number(file_allocation)
        file_allocation[first_free_slot] = file_allocation[last_position_of_last_number]
        file_allocation[last_position_of_last_number] = "."
        resorted = "".join(file_allocation)
    print(resorted)
    checksum = 0
    for index in range(len(file_allocation)):
        if file_allocation[index] == ".":
            break
        # print(int(file_allocation[index]))
        checksum += int(file_allocation[index]) * index
    print(f"The checksum is {checksum}")


if __name__ == "__main__":
    main()

#91380424522 too low
#86736900704 too low
#6432869891895 correct