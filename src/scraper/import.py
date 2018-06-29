import logging
import os

import dateutil
import pandas as pd
from tqdm import tqdm

from src import DATA_FOLDER
from src.db.model import db, AlreadyReadFile, Wave, Tide, Weather, \
    Wind
from src.scraper.scrap import DATASETS

DATA_FILES = set([os.path.join(DATA_FOLDER, file)
                  for file in os.listdir(DATA_FOLDER) if ".csv.gz" in file])


def already_imported_files():
    return {arf.filename for arf in db.session.query(AlreadyReadFile)}


def not_already_imported_files():
    return DATA_FILES - already_imported_files()


def get_files(dataset_name):
    assert dataset_name in DATASETS
    files = \
        set(filter(lambda n: dataset_name in n, not_already_imported_files()))
    return files


def import_dataset(dataset_name, table):
    files = get_files(dataset_name=dataset_name)
    logging.info("{nb_files} files to import in {table_name}.   "
                 .format(nb_files=len(files), table_name=table.__name__))
    n_new = 0
    n_old = 0
    for f in tqdm(sorted(files)):
        spot_id = f.split("_")[-1].split(".")[0]
        df = pd.read_csv(f)
        records = df.to_dict(orient="records")
        _n_new, _n_old = upsert_records(records, spot_id, table)
        db.session.add(AlreadyReadFile(filename=f))
        n_new = _n_new
        n_old = _n_old
        db.session.commit()
    logging.info("Inserted {n_new} / updated {n_old} records in {table_name}."
                 .format(n_new=n_new, n_old=n_old, table_name=table.__name__))


def upsert_records(records, spot_id, table):
    new_timestamps = set()
    new_records_dict = {}
    for r in records:
        new_r = table(spot_id=spot_id, **r)
        new_r.timestamp = dateutil.parser.parse(new_r.timestamp)
        new_records_dict[new_r.timestamp.isoformat()] = new_r
        new_timestamps.add(new_r.timestamp)
    query = db.session.query(table) \
        .filter_by(spot_id=spot_id) \
        .filter(table.timestamp.in_(new_timestamps))
    n_old = query.count()
    for old_record in query:
        timestamp = old_record.timestamp.isoformat()
        if timestamp not in new_records_dict:
            # ToDo
            continue
        w = new_records_dict.pop(timestamp)
        w.id = old_record.id
        db.session.merge(w)
    db.session.add_all(new_records_dict.values())
    return len(new_records_dict), n_old


def main():
    from src.api.app import app
    with app.app_context():
        logging.info("Start importing.")
        import_dataset("wave", Wave)
        # import_dataset("conditions", Conditions)
        import_dataset("tides", Tide)
        import_dataset("weather", Weather)
        import_dataset("wind", Wind)
        logging.info("Import finished.")


if __name__ == "__main__":
    main()
