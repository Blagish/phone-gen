from flask import Flask
from app.config import Config
import logging


providers = set()
regions = set()
city_by_region = dict()
data_by_region = list()
providers_by_region = dict()


logger = logging.getLogger('PhoneGen')
logger.setLevel(logging.INFO)
fh = logging.FileHandler("phonegen.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)


from app.get_csv import load_database  # this looks terrible but is sufficient

app = Flask(__name__)
app.config.from_object(Config)
logger.info('Starting the app...')
load_database(update=False)

from app import routes
