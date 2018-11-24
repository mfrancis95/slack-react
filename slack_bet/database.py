from pymongo import MongoClient
from os import environ
from datetime import datetime, timedelta

try:
    _bets = MongoClient(f'mongodb://{environ["MONGODB_USER"]}:{environ["MONGODB_PASSWORD"]}@{environ.get("MONGODB_HOST", "localhost")}/{environ["MONGODB_DATABASE"]}').bet.bets
except:
    _bets = MongoClient().bet.bets

def insert_reaction(channel, timestamp):
    _bets.insert_one({
        'channel': channel,
        'timestamp': datetime.utcfromtimestamp(float(timestamp))
    })

def get_top_reactions(top):
    today = datetime.utcnow()
    aggregation = [
        {'$group': {'_id': '$channel', 'count': {'$sum': 1}}},
        {'$group': {'_id': '$count', 'channels': {'$push': '$_id'}}},
        {'$sort': {'_id': -1}},
        {'$limit': 5}
    ]
    if top:
        if top == 'month':
            top = timedelta(days = 30)
        elif top == 'week':
            top = timedelta(weeks = 1)
        elif top == 'year':
            top = timedelta(days = 365)
        else:
            top = timedelta(days = 1)
        aggregation = [
            {'$match': {'timestamp': {'$gt': today - top, '$lte': today}}}
        ] + aggregation
    return _bets.aggregate(aggregation)