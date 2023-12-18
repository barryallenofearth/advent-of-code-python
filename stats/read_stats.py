import re

import bs4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import scipy.optimize
from matplotlib.ticker import MaxNLocator


def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b


data = pd.DataFrame([], columns=["year", "day", "both_stars", "single_star"])
year_with_half_life = pd.DataFrame([], columns=["year", "half_life_time"])

for current_year in range(2015, 2024):
    print(f"parse year {current_year}")
    result = requests.get(f"https://adventofcode.com/{current_year}/stats")
    soup = bs4.BeautifulSoup(result.text, features="html.parser")
    stats_anchor_links = soup.select(".stats a")

    for stats_anchor_link in stats_anchor_links:
        values = re.split(r"\s+", stats_anchor_link.text)
        increment_length = 0
        if len(values[0]) == 0:
            increment_length = 1
        day = values[0 + increment_length]
        both_stars = values[1 + increment_length]
        single_star = values[2 + increment_length]

        data.loc[len(data)] = [int(current_year), int(day), int(both_stars), int(single_star)]

    year_frame = data[data["year"] == current_year]
    year_frame.sort_values("day")

    year_frame.plot.scatter(x="day", y="both_stars")

    p0 = (2000, .1, 50)  # start with values near those we expect
    params, cv = scipy.optimize.curve_fit(monoExp, year_frame["day"], year_frame["both_stars"], p0)

    m, t, b = params
    plt.plot(year_frame["day"], monoExp(year_frame["day"], m, t, b), '--', label="fitted")

    plt.title(f"Both stars {current_year}")
    plt.xlabel("Day")
    plt.ylabel("#Users solving both parts")
    plt.show()

    current_year_with_halt_time = [current_year, np.log(2) / t]
    year_with_half_life.loc[len(year_with_half_life)] = current_year_with_halt_time
    plt.savefig(f'{current_year}_both_stars.png', bbox_inches="tight")
# print(data)
print(year_with_half_life)
pd.options.display.float_format = '{:,.0f}'.format
year_with_half_life.plot.bar(x="year", y="half_life_time")
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Year")
plt.ylabel("Both stars count half life time (d)")
plt.show()
