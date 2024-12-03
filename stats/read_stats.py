import datetime
import re

import bs4
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import requests
import scipy.optimize


def exponential_function(x, y_0, t_half: float, offset: float):
    return y_0 * np.exp(- np.log(2) / t_half * (x - 1)) + offset


data = pd.DataFrame([], columns=["year", "day", "both_stars", "single_star"])
year_with_half_life = pd.DataFrame([], columns=["year", "half_life_time"])
year_with_total_count = pd.DataFrame([], columns=["year", "total_count"])
year_with_user_day1_count = pd.DataFrame([], columns=["year", "user_day1_count"])
year_with_user_day25_count = pd.DataFrame([], columns=["year", "user_day25_count"])

starting_year = 2015
latest_year = datetime.date.today().year
for current_year in range(starting_year, latest_year + 1):
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

    data_bar_chart = go.Bar(x=year_frame["day"], y=year_frame["both_stars"], name="Both stars", marker_color="#e39032", marker_line_color='black', marker_line_width=2, opacity=1)

    initial_parameters = (year_frame["both_stars"].iloc[0], 4, 0)  # start with values near those we expect
    params, cv = scipy.optimize.curve_fit(exponential_function, year_frame["day"], year_frame["both_stars"], initial_parameters)

    y_0, t_half, offset = params
    fit_x_values = [x / 100 for x in range(100, len(year_frame) * 100)]
    fit_trace = go.Scatter(x=fit_x_values, y=[exponential_function(x, y_0, t_half, offset) for x in fit_x_values], mode='lines', name='Fit', line_color="#281ed9", line_width=3)

    figure = go.Figure(data=[data_bar_chart, fit_trace],
                       layout={"title": f"Both stars {current_year}", "xaxis": {'title': {'text': "Day"}}, "yaxis": {'title': {'text': "Users solving both parts (#)"}}})
    figure.add_annotation(text=f'Half life time: {t_half:2.2f} days', align='left', showarrow=False, xref='paper', yref='paper', x=0.5, y=0.8, bordercolor='black', borderwidth=1)
    figure.write_image(f'{current_year}_both_stars.png')

    year_with_half_life.loc[len(year_with_half_life)] = [int(current_year), t_half]
    year_with_total_count.loc[len(year_with_total_count)] = [int(current_year), year_frame["both_stars"].sum()]
    year_with_user_day1_count.loc[len(year_with_user_day1_count)] = [int(current_year),
                                                                     year_frame[year_frame["day"] == 1]["single_star"].values[0] + year_frame[year_frame["day"] == 1]["both_stars"].values[0]]
    if len(year_frame) == 25:
        year_with_user_day25_count.loc[len(year_with_user_day25_count)] = [int(current_year), year_frame[year_frame["day"] == 25]["both_stars"].values[0]]

bar_chart = go.Bar(x=year_with_half_life["year"], y=year_with_half_life["half_life_time"], name="half life time", marker_color="#e39032", marker_line_color='black', marker_line_width=2, opacity=1)
average_t_half = year_with_half_life["half_life_time"].mean()
average_trace = go.Scatter(x=[starting_year - 0.5, latest_year + 0.5], y=[average_t_half, average_t_half], mode='lines', name='Average Value', line=dict(color='#281ed9', width=3, dash='dash'))
half_life_image = go.Figure(data=[bar_chart, average_trace],
                            layout={"title": f"Half life time per year", "xaxis": {'title': {'text': "Year"}}, "yaxis": {'title': {'text': "Half life time (day)"}}})
half_life_image.add_annotation(text=f"&#8709;={average_t_half:2.2f} day", align='left', showarrow=False, xref='paper', yref='paper', x=0.5, y=1.2, bordercolor='black', borderwidth=1)
half_life_image.write_image(f'comparison_both_stars.png')

total_count_bar_chart = go.Bar(x=year_with_total_count["year"], y=year_with_total_count["total_count"], name="total solved 2 stars", marker_color="#e39032",
                               marker_line_color='black', marker_line_width=2, opacity=1)
total_count_image = go.Figure(data=[total_count_bar_chart],
                              layout={"title": f"Total 2 star count per year", "xaxis": {'title': {'text': "Year"}}, "yaxis": {'title': {'text': "Total 2 star count"}}})
total_count_image.write_image(f'both_stars_total_count_per_year.png')

day1_count_bar_chart = go.Bar(x=year_with_user_day1_count["year"], y=year_with_user_day1_count["user_day1_count"], name="users solving day 1 part 1", marker_color="#e39032",
                              marker_line_color='black', marker_line_width=2, opacity=1)
day1_count_image = go.Figure(data=[day1_count_bar_chart],
                             layout={"title": f"Users count per year", "xaxis": {'title': {'text': "Year"}}, "yaxis": {'title': {'text': "Users solving day 1 part 1"}}})
day1_count_image.write_image(f'users_per_year.png')

completing_percentage = pd.DataFrame(
    {"year": year_with_user_day1_count["year"], "completion_ratio": year_with_user_day25_count["user_day25_count"] / year_with_user_day1_count["user_day1_count"] * 100})

completing_percentage_bar_chart = go.Bar(x=completing_percentage["year"], y=completing_percentage["completion_ratio"], name="users completing all riddles", marker_color="#e39032",
                                         marker_line_color='black', marker_line_width=2, opacity=1)
completing_percentage_image = go.Figure(data=[completing_percentage_bar_chart],
                                        layout={"title": f"Users completing all riddles per year", "xaxis": {'title': {'text': "Year"}},
                                                "yaxis": {'title': {'text': "Part of users solving all riddles (%)"}}})
completing_percentage_image.write_image(f'completing_percentage_per_year.png')
