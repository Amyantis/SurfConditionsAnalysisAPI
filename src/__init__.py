import logging
from os.path import join

DATA_FOLDER = "/home/tdancois/PycharmProjects/SurfConditionsAnalysisAPI/data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(filename=join(DATA_FOLDER, "scraper.log")),
        logging.StreamHandler()
    ],
)

LACANAU_SPOT_ID = "5842041f4e65fad6a7708c8d"
SPOT_IDS = {LACANAU_SPOT_ID}
