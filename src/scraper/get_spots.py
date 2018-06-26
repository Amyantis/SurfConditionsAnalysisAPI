import json
import logging
from urllib.request import urlopen

import pandas as pd

from src.db.model import Spot, db

URL = "https://services.surfline.com/kbyg/mapview?south=-90&west=-180&north=90&east=180"


def get_data():
    logging.info("Downloading %s...", URL)
    with urlopen(URL) as fdesc:
        data = fdesc.read()
        logging.info("Download and read completed.")
        return json.loads(data.decode("utf8"))


def parse_data(json_data):
    df_spots = pd.io.json.json_normalize(json_data["data"]["spots"])
    return df_spots


def import_spots(df_spots):
    logging.info("Import %d spots.", len(df_spots))
    db.session.add_all((
        Spot(api_id=spot._id, name=spot["name"], latitude=spot.lat,
             longitude=spot.lon) for idx, spot in df_spots.iterrows()))
    db.session.commit()
    logging.info("Spots import successful.")


def main():
    from src.api.app import app
    with app.app_context():
        db.session.query(Spot).delete()
        import_spots(parse_data(get_data()))


if __name__ == "__main__":
    main()
