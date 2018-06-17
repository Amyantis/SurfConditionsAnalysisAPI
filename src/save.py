import logging
from datetime import datetime
from os.path import join

from src import DATA_FOLDER, SPOT_IDS
from src.scrap import get_tides_data, get_wind_data, get_weather_data, \
    get_wave_data


def main():
    for spot_id in SPOT_IDS:
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
        df_wave.to_csv(path_or_buf=path, compression='gzip')
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
        df_weather.to_csv(path_or_buf=path, compression='gzip')
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
        df_wind.to_csv(path_or_buf=path, compression='gzip')
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
        df_tides.to_csv(path_or_buf=path, compression='gzip')
        logging.info("Tides data saved.")
    except Exception as e:
        logging.error(type(e), e)
    logging.info("Finished.")


if __name__ == "__main__":
    main()
