from flask import Flask
from app.config import Config


providers = set()
regions = set()
city_by_region = dict()
data_by_region = list()

from app.get_csv import update_database #İÒÎ ÓÆÀÑÍÎ ÍÅÊĞÀÑÈÂÎ ÍÎ ÒÀÊ ÍÀÄÎ

app = Flask(__name__)
app.config.from_object(Config)

update_database()

from app import routes#, models
