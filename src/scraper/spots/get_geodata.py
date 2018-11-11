import logging
from time import sleep

import geocoder

from src.model import db, Spot


def update_geodata(spot):
    g = geocoder.osm([spot.latitude, spot.longitude], method='reverse')
    spot.city = g.city
    spot.state = g.state
    spot.country = g.country


def update_all_geodata():
    for i, spot in enumerate(db.session.query(Spot).filter_by(country=None)):
        update_geodata(spot)
        sleep(1)
        if i % 100:
            logging.info("Updating 100 spots geodata.")
            db.session.commit()
    db.session.commit()


def main():
    from src.app import app
    with app.app_context():
        update_all_geodata()


if __name__ == "__main__":
    main()
