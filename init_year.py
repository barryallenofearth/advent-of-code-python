import os
import time

year = input("Please enter the year you want to initialize")
if not os.path.exists(year):
    print(f"Initialize year {year}")
    os.mkdir(year)
    time.sleep(3)
    with open(f"aoc_{year}/__init__.py", "w") as file:
        print("create package init")

    for day in range(1, 26):
        os.mkdir(f"aoc_{year}/day{day}")
        os.mkdir(f"aoc_{year}/day{day}/common")
        with open(f"aoc_{year}/day{day}/common/.gitkeep", "w"):
            print(f"create common folder .gitkeep file")
        with open(f"aoc_{year}/day{day}/riddle.txt", "w"):
            print(f"create package aoc_{year}/day{day}/riddle.txt")
        for part in range(1, 3):
            part_path = f"aoc_{year}/day{day}/part{part}"
            os.makedirs(part_path)

            main_file = f"{part_path}/main_{day}_{part}.py"
            with open(main_file, "w"):
                print(f"create file {main_file}")
