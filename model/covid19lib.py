import datetime as dt

import pandas as pd
import numpy as np


WINDOW_LEN = 36
WINDOW_OFFSET = 7

URL_DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
URL_CASES = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
URL_RECOVERIES = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

EU = [
    'Germany',
    'France',
    'Italy',
    'Spain',
    'Poland',
    'Romania',
    'Bulgaria',
    'Hungary',
    'Czechia',
    'Austria',
    'Portugal',
    'Denmark',
    'Croatia',
    'Lithuania',
    'Belgium',
]


def get_dfs(validation_split=7):
    deaths = pd.read_csv(URL_DEATHS)
    recoveries = pd.read_csv(URL_RECOVERIES)
    cases = pd.read_csv(URL_CASES)
        
    del deaths['Lat']
    del deaths['Long']

    del recoveries['Lat']
    del recoveries['Long']

    del cases['Lat']
    del cases['Long']

    region = EU

    deaths = deaths[deaths['Country/Region'].isin(region) & deaths['Province/State'].isna()]
    recoveries = recoveries[recoveries['Country/Region'].isin(region) & recoveries['Province/State'].isna()]
    cases = cases[cases['Country/Region'].isin(region) & cases['Province/State'].isna()]

    del deaths['Province/State']
    del recoveries['Province/State']
    del cases['Province/State']

    keys = list(deaths.keys())

    drop_keys = keys[-validation_split:]
    validation_keys = ['Country/Region'] + keys[-WINDOW_LEN - WINDOW_OFFSET + 1 - validation_split:]

    deaths_validation = deaths[validation_keys]
    recoveries_validation = recoveries[validation_keys]
    cases_validation = cases[validation_keys]

    deaths = deaths.drop(drop_keys, axis=1)
    recoveries = recoveries.drop(drop_keys, axis=1)
    cases = cases.drop(drop_keys, axis=1)

    return deaths, recoveries, cases, deaths_validation, recoveries_validation, cases_validation

def get_ds(deaths, recoveries, cases):
    del deaths['Country/Region']
    del recoveries['Country/Region']
    del cases['Country/Region']

    deaths = deaths.to_numpy().astype(np.int64)
    recoveries = recoveries.to_numpy().astype(np.int64)
    cases = cases.to_numpy().astype(np.int64)

    data = []

    for x_idx in range(deaths.shape[1] - WINDOW_LEN - WINDOW_OFFSET):
        for jdx in range(deaths.shape[0]):
            deaths_row = deaths[jdx,x_idx: x_idx + WINDOW_LEN + WINDOW_OFFSET]
            recoveries_row = recoveries[jdx,x_idx: x_idx + WINDOW_LEN + WINDOW_OFFSET]
            cases_row = cases[jdx,x_idx: x_idx + WINDOW_LEN + WINDOW_OFFSET]

            if any([(cell < 20).any() for cell in [deaths_row, recoveries_row, cases_row]]):
                continue

            X_deaths = deaths_row[:WINDOW_LEN]
            X_recoveries = recoveries_row[:WINDOW_LEN]
            X_cases = cases_row[:WINDOW_LEN]

            if any([len(cell) != WINDOW_LEN for cell in [X_deaths, X_recoveries, X_cases]]):
                raise Exception('')

            y_deaths = deaths_row[WINDOW_LEN + WINDOW_OFFSET - 1]
            y_recoveries = recoveries_row[WINDOW_LEN + WINDOW_OFFSET - 1]
            y_cases = cases_row[WINDOW_LEN + WINDOW_OFFSET - 1]

            data.append([X_deaths, X_recoveries, X_cases, y_deaths, y_recoveries, y_cases])

    X = np.vstack([np.hstack(row[:3]) for row in data])
    y = np.hstack([row[3] for row in data])

    return X, y

def convert_dfs(deaths, recoveries, cases):
    ret = []
    dates = list(deaths.keys())[1:]

    for idx in range(len(deaths)):
        country = deaths['Country/Region'].iat[idx]

        deaths_row = deaths.iloc[idx]
        recoveries_row = recoveries.iloc[idx]
        cases_row = cases.iloc[idx]

        for jdx in range(len(dates)):
            date = dates[jdx]

            ret.append({
                'country': country,
                'date': date,
                'deaths': int(deaths_row[date]),
                'recoveries': int(recoveries_row[date]),
                'cases': int(cases_row[date])})

    return  ret
