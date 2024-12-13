import re


class SpaceDefinition:

    def __init__(self, id: int, length: int, is_file: bool):
        self.id = id
        self.length = length
        self.is_file = is_file

    def __repr__(self):
        return f"SpaceDefinition({self.id}, {self.length}, {self.is_file})"


def main():
    def find_lowest_space(disk_definitions: list[SpaceDefinition], file_definition: SpaceDefinition):
        file_location = diskspace_definitions.index(file_definition)
        for index in range(file_location):
            if not disk_definitions[index].is_file and disk_definitions[index].length >= file_definition.length:
                return index
        return -1

    def combine_allocation(diskspace_definitions: list[SpaceDefinition]) -> list[str]:
        complete_allocation = []
        for disk_definition in diskspace_definitions:
            for _ in range(disk_definition.length):
                if disk_definition.is_file:
                    complete_allocation.append(f"{disk_definition.id}")
                else:
                    complete_allocation.append(".")

        return complete_allocation

    TEST_MODE = False
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    diskspace_definitions = []
    file_definitions = []
    with open(file_name, encoding="utf-8") as riddle_input:
        for line in riddle_input:
            line = line.strip()

        for index in range(len(line)):
            number = int(line[index])
            file_index = int(index / 2)
            if index % 2 == 0:
                diskspace_definitions.append(SpaceDefinition(file_index, number, True))
                file_definitions.append(diskspace_definitions[-1])

            else:
                diskspace_definitions.append(SpaceDefinition(file_index, number, False))

    complete_allocation = combine_allocation(diskspace_definitions)
    print(''.join(complete_allocation))

    file_definitions = file_definitions[::-1]
    for file_definition in file_definitions:
        lowest_space_index_matching = find_lowest_space(diskspace_definitions, file_definition)
        if lowest_space_index_matching == -1:
            continue

        space_definition = diskspace_definitions[lowest_space_index_matching]
        file_location = diskspace_definitions.index(file_definition)
        file_index += 1
        diskspace_definitions[file_location] = SpaceDefinition(file_index, file_definition.length, False)

        if space_definition.length == file_definition.length:
            diskspace_definitions[lowest_space_index_matching] = file_definition
        else:
            diskspace_definitions.insert(lowest_space_index_matching, file_definition)
            space_definition.length -= file_definition.length

        complete_allocation = combine_allocation(diskspace_definitions)
        # print(''.join(complete_allocation))

    checksum = 0
    for index in range(len(complete_allocation)):
        if complete_allocation[index] == ".":
            continue
        checksum += int(complete_allocation[index]) * index
    print(f"The checksum is {checksum}")


if __name__ == "__main__":
    main()

# 91380424522 too low
# 86736900704 too low
# 6432869891895 correct
