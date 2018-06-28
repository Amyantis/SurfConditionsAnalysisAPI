import logging
import os

DATA_FOLDER = os.environ['DATA_FOLDER']

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(filename=os.path.join(DATA_FOLDER, "%s.log" % __name__)),
        logging.StreamHandler()
    ],
)
