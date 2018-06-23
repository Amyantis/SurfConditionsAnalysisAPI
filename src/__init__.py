import logging
from os.path import join

DATA_FOLDER = "/home/tdancois/PycharmProjects/SurfConditionsAnalysisAPI/data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(filename=join(DATA_FOLDER, "%s.log" % __name__)),
        logging.StreamHandler()
    ],
)
