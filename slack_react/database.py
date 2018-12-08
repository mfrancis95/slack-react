from pymongo import MongoClient
from os import environ
from datetime import datetime, timedelta

try:
    _reactions = MongoClient(f'mongodb://{environ["MONGODB_USER"]}:{environ["MONGODB_PASSWORD"]}@{environ.get("MONGODB_HOST", "localhost")}/{environ["MONGODB_DATABASE"]}')[environ['MONGODB_DATABASE']].reactions
except:
    _reactions = MongoClient()[environ['MONGODB_DATABASE']].reactions

def insert_reaction(channel, user, timestamp):
    _reactions.insert_one({
        'channel': channel,
        'user': user,
        'timestamp': datetime.utcfromtimestamp(float(timestamp))
    })

def get_top_reactions(field, top):
    today = datetime.utcnow()
    aggregation = [
        {'$group': {'_id': f'${field}', 'count': {'$sum': 1}}},
        {'$group': {'_id': '$count', 'ids': {'$push': '$_id'}}},
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
    return _reactions.aggregate(aggregation)