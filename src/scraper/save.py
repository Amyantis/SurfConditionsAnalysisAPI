import logging
from datetime import datetime
from multiprocessing.pool import Pool
from os.path import join

from tqdm import tqdm

from src import DATA_FOLDER
from src.db.datasets import available_spots
from src.scraper.scrap import get_tides_data, get_wind_data, get_weather_data, \
    get_wave_data, get_conditions_data


def spot_set():
    from src.api.app import app
    with app.app_context():
        return available_spots()


def main():
    s = spot_set()
    with Pool(12) as p:
        for _ in tqdm(p.imap(get_all_datasets, s), total=len(s)):
            pass


def main_using_monothread():
    for spot_id in spot_set():
        get_all_datasets(spot_id)


def get_all_datasets(spot_id):
    current_time = datetime.now().isoformat()
    logging.info("Starting to get the data (spot: `%s`), current time: %s.",
                 spot_id, current_time)
    try:
        logging.info("Starting to get wave data (spot: `%s`).", spot_id)
        df_wave = get_wave_data(spot_id)
        filename = "wave_{current_time}_{spot_id}.csv.gz" \
            .format(current_time=current_time, spot_id=spot_id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_wave.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Wave data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get weather data (spot: `%s`).", spot_id)
        df_weather = get_weather_data(spot_id)
        filename = "weather_{current_time}_{spot_id}.csv.gz" \
            .format(current_time=current_time, spot_id=spot_id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_weather.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Weather data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get wind data (spot: `%s`).", spot_id)
        df_wind = get_wind_data(spot_id)
        filename = "wind_{current_time}_{spot_id}.csv.gz" \
            .format(current_time=current_time, spot_id=spot_id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_wind.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Wind data saved.")
    except Exception as e:
        logging.error(type(e), e)
    try:
        logging.info("Starting to get tides data (spot: `%s`).", spot_id)
        df_tides = get_tides_data(spot_id)
        filename = "tides_{current_time}_{spot_id}.csv.gz" \
            .format(current_time=current_time, spot_id=spot_id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_tides.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Tides data saved.")
    except Exception as e:
        logging.error(type(e), e)
    logging.info("Finished.")
    try:
        logging.info("Starting to get conditions data (spot: `%s`).", spot_id)
        df_conditions = get_conditions_data(spot_id)
        filename = "conditions_{current_time}_{spot_id}.csv.gz" \
            .format(current_time=current_time, spot_id=spot_id)
        path = join(DATA_FOLDER, filename)
        logging.info("Saving data to %s.", path)
        df_conditions.to_csv(path_or_buf=path, compression='gzip', index=False)
        logging.info("Conditions data saved.")
    except Exception as e:
        logging.error(type(e), e)
    logging.info("Finished.")


if __name__ == "__main__":
    main()
