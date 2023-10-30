import pymongo
import json

with open('src/config/config.json', "r") as e:
    config = json.load(e)

database = pymongo.MongoClient(config['mongoUrl'])