"""
This method excepts strings and lists of strings and returns a dict of a letters and the number of times they were encountered
"""
def count_chars_in_string(char_sequence):
    counted_chars = {}
    for index in range(0, len(char_sequence)):
        char = char_sequence[index]
        if char in counted_chars:
            continue
        counted_chars[char] = 1

        for reference_index in range(0, len(char_sequence)):
            if index == reference_index:
                continue

            if char == char_sequence[reference_index]:
                counted_chars[char] = counted_chars[char] + 1

    return counted_chars


def sort_counted_chars(counted_chars: dict, use_char_value_as_tie_breaker=True):
    list_of_counted_chars = [item for item in counted_chars.items()]
    if use_char_value_as_tie_breaker:
        list_of_counted_chars.sort(key=lambda x: (-x[1], x[0]))
    else:
        list_of_counted_chars.sort(key=__sorting_parameter)

    return list_of_counted_chars


def __sorting_parameter(char_and_count: tuple):
    return char_and_count[1]
