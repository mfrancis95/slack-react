from pymongo import MongoClient
from os import environ
from datetime import datetime, timedelta

try:
    _bets = MongoClient(f'mongodb://{environ["MONGODB_USER"]}:{environ["MONGODB_PASSWORD"]}@{environ.get("MONGODB_HOST", "localhost")}/{environ["MONGODB_DATABASE"]}').bet.bets
except:
    _bets = MongoClient().bet.bets

def bet(channel, timestamp):
    _bets.insert_one({'channel': channel, 'timestamp': datetime.utcfromtimestamp(float(timestamp))})

def get_top_bets():
    today = datetime.utcnow()
    yesterday = today - timedelta(days = 1)
    return _bets.aggregate([
        {'$match': {'timestamp': {'$gt': yesterday, '$lte': today}}},
        {'$group': {'_id': '$channel', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ])