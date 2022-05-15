import imp
import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config('MONGO_URI'))

db = client['Be-caribeDatabase']
var = db.device.find({'device_name': 'device1', 'graph_data.date': {'$gte': datetime(2022,5,15) }})
for i in var:
    print(i)
