import os
import time

year = input("Please enter the year you want to initialize")
if not os.path.exists(f"aoc_{year}"):
    print(f"Initialize year {year}")
    os.mkdir(f"aoc_{year}")
    time.sleep(3)
    with open(f"aoc_{year}/__init__.py", "w") as file:
        print("create package init")

    for day in range(5, 26):
        os.mkdir(f"aoc_{year}/day{day}")
        with open(f"aoc_{year}/day{day}/riddle.txt", "w"):
            print(f"create package aoc_{year}/day{day}/riddle.txt")
        with open(f"aoc_{year}/day{day}/test_riddle.txt", "w"):
            print(f"create package aoc_{year}/day{day}/test_riddle.txt")
        for part in range(1, 3):
            part_path = f"aoc_{year}/day{day}/part{part}"
            os.makedirs(part_path)

            main_file = f"{part_path}/main_{day}_{part}.py"
            with open(main_file, "w",encoding="utf-8") as main_file:
                main_file.write('TEST_MODE = True\nif TEST_MODE:\n    file_name = "../test_riddle.txt"\nelse:\n    file_name = "../riddle.txt"\n')
                print(f"create file {main_file}")
