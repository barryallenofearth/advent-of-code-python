def main():
    TEST_MODE = True
    if TEST_MODE:
        file_name = "../test_riddle.txt"
    else:
        file_name = "../riddle.txt"
    with open(file_name, encoding="utf-8") as riddle_input:
        for line in riddle_input:
            line = line.strip()


if __name__ == "__main__":
    main()
