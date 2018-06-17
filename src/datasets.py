import os

import pandas as pd

from src import DATA_FOLDER
from src.scrap import DATASETS

DATA_FILES = sorted([os.path.join(DATA_FOLDER, file)
                     for file in os.listdir(DATA_FOLDER) if ".csv.gz" in file])


def make_complete_df(dataset_name):
    assert dataset_name in DATASETS
    files = list(filter(lambda n: dataset_name in n, DATA_FILES))
    dfs = (pd.read_csv(f) for f in files)
    df = pd.concat(dfs, ignore_index=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.drop_duplicates(keep="last", inplace=True)
    df.timestamp = pd.to_datetime(df.timestamp, utc=True)
    return df


def get_wave_df():
    return make_complete_df(dataset_name="wave")


def get_weather_df():
    return make_complete_df(dataset_name="weather")


def get_conditions_df():
    return make_complete_df(dataset_name="conditions")


def get_wind_df():
    return make_complete_df(dataset_name="wind")


def get_tides_df():
    return make_complete_df(dataset_name="tides")
