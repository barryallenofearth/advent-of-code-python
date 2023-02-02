from util.strings import string_utils


def read_and_group_signal(search_most_common_letter=True):
    if search_most_common_letter:
        index = 0
    else:
        index = -1
    with open("../riddle.txt") as file:
        all_lines = file.readlines()
        all_columns = [[line[column] for line in all_lines] for column in range(0, len(all_lines[0]) - 1)]

        all_most_repeated_chars = [string_utils.sort_counted_chars(string_utils.count_chars_in_string(all_columns[column]))[index][0] for column in range(0, len(all_columns))]

    return "".join(all_most_repeated_chars)
