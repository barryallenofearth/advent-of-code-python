RIDDLE_FILE = "riddle.txt"
TEST_RIDDLE_FILE = "test_riddle.txt"
TEST_2_RIDDLE_FILE = "test2_riddle.txt"


def read_file(riddle_file_name: str) -> list[str]:
    with open(f"{riddle_file_name}", encoding="utf-8") as file:
        return [line.strip() for line in file]
