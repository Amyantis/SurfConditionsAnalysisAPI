import logging
from datetime import datetime
from multiprocessing.pool import Pool
from os.path import join

from tqdm import tqdm

from src import DATA_FOLDER
from src.model import db, Spot
from src.scraper.weather.scrap import get_tides_data, get_wind_data, get_weather_data, \
    get_wave_data, get_conditions_data


def spots():
    from src.app import app
    with app.app_context():
        return db.session.query(Spot)


def main():
    s = list(spots())
    with Pool(8) as p:
        for _ in tqdm(p.imap(get_all_datasets, s), total=len(s)):
            pass


def main_using_monothread():
    for spot in spots():
        get_all_datasets(spot)


def get_all_datasets(spot):
    current_time = datetime.now().isoformat()
    logging.info("Starting to get the data (spot: `%s`), current time: %s.",
                 spot.id, current_time)
    try:
        logging.info("Starting to get wave data (spot: `%s`).", spot.id)
        df_wave = get_wave_data(spot.api_id)
        filename = "wave_{current_time}_{spot_id}.csv.gz".format(
            current_time=current_time, spot_id=spot.id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_wave.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Wave data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get weather data (spot: `%s`).", spot.id)
        df_weather = get_weather_data(spot.api_id)
        filename = "weather_{current_time}_{spot_id}.csv.gz".format(
            current_time=current_time, spot_id=spot.id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_weather.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Weather data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get wind data (spot: `%s`).", spot.id)
        df_wind = get_wind_data(spot.api_id)
        filename = "wind_{current_time}_{spot_id}.csv.gz".format(
            current_time=current_time, spot_id=spot.id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_wind.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Wind data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get tides data (spot: `%s`).", spot.id)
        df_tides = get_tides_data(spot.api_id)
        filename = "tides_{current_time}_{spot_id}.csv.gz".format(
            current_time=current_time, spot_id=spot.id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_tides.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Tides data saved.")
    except Exception as e:
        logging.error(type(e), e)
    logging.info("Finished.")
    try:
        logging.info("Starting to get conditions data (spot: `%s`).", spot.id)
        df_conditions = get_conditions_data(spot.api_id)
        filename = "conditions_{current_time}_{spot_id}.csv.gz".format(
            current_time=current_time, spot_id=spot.id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_conditions.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Conditions data saved.")
    except Exception as e:
        logging.error(type(e), e)
    logging.info("Finished.")


if __name__ == "__main__":
    import os

    if "MULTITHREAD" in os.environ:
        main_using_monothread()
    else:
        main()
