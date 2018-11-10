import logging
import os

DATA_FOLDER = os.environ.get('DATA_FOLDER', default="/data")
SQLALCHEMY_DATABASE_URI = \
    os.environ.get('SQLALCHEMY_DATABASE_URI', default='postgresql://postgres:postgres@localhost:54322/surfdb')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s")

logging.info("DATA_FOLDER=%s", DATA_FOLDER)
logging.info("SQLALCHEMY_DATABASE_URI=%s", SQLALCHEMY_DATABASE_URI)
