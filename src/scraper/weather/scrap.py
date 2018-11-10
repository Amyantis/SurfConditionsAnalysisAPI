import json
import logging
from urllib.request import urlopen

import pandas as pd
from pandas.io.json import json_normalize

URL = "https://services.surfline.com/kbyg/spots/forecasts/" \
      "{dataset}?spotId={spot_id}&days={nb_days}&intervalHours={interval_hours}"

DATASETS = {"weather", "conditions", "tides", "wind", "wave"}

UTC_OFFSET = pd.Timedelta(hours=2)

INTERVAL_HOURS = 1
NB_DAYS = 6


def get_data(spot_id, dataset, nb_days=NB_DAYS, interval_hours=INTERVAL_HOURS):
    assert dataset in DATASETS
    url = URL.format(
        spot_id=spot_id,
        dataset=dataset,
        nb_days=nb_days,
        interval_hours=interval_hours)
    logging.info("Downloading %s...", url)
    with urlopen(url) as fdesc:
        data = fdesc.read()
        logging.info("Download and read completed.")
        return json.loads(data.decode("utf8"))


def parse_timestamp_column(timestamp_series):
    return pd.to_datetime(timestamp_series, unit='s', utc=True) + UTC_OFFSET


def get_wave_data(spot_id):
    wave_data = get_data(spot_id, "wave")
    df_wave = json_normalize(wave_data["data"]["wave"], sep="_")
    df_wave.timestamp = parse_timestamp_column(df_wave.timestamp)
    for i in range(len(df_wave.swells[0])):
        data_swell_i = json_normalize(
            df_wave.swells.apply(lambda x: x[i]), sep="_")
        data_swell_i.columns = \
            data_swell_i.columns.map(lambda x: "wave_%s_%d" % (x, i))
        df_wave = df_wave.join(data_swell_i, how='left')
    df_wave.drop(columns=["swells"], inplace=True)
    return df_wave


def get_weather_data(spot_id):
    weather_data = get_data(spot_id, "weather")
    df_weather = json_normalize(weather_data["data"]["weather"], sep="_")
    df_weather.timestamp = parse_timestamp_column(df_weather.timestamp)
    return df_weather


def get_wind_data(spot_id):
    wind_data = get_data(spot_id, "wind")
    df_wind = json_normalize(wind_data["data"]["wind"], sep="_")
    df_wind.timestamp = parse_timestamp_column(df_wind.timestamp)
    return df_wind


def get_tides_data(spot_id):
    tides_data = get_data(spot_id, "tides")
    df_tides = json_normalize(tides_data["data"]["tides"], sep="_")
    df_tides.timestamp = parse_timestamp_column(df_tides.timestamp)
    return df_tides


def get_conditions_data(spot_id):
    conditions_data = get_data(spot_id, "conditions")
    df_conditions = \
        json_normalize(conditions_data["data"]["conditions"], sep="_")
    df_conditions.timestamp = parse_timestamp_column(df_conditions.timestamp)
    return df_conditions
