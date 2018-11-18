from os import environ
from requests import get, post
from re import IGNORECASE, search
from flask import request

def get_channel(channel):
    arguments = {
        'channel': channel,
        'token': environ['OAUTH_TOKEN']
    }
    return get('https://slack.com/api/channels.info', arguments).json()['channel']['name']

def _message():
    try:
        if search(environ['REGEX'], request.json['event']['text'], IGNORECASE):
            _react(request.json['event']['channel'], request.json['event']['ts'])
    except:
        pass

def _react(channel, timestamp):
    arguments = {
        'channel': channel,
        'name': environ['REACTION'],
        'timestamp': timestamp,
        'token': environ['OAUTH_TOKEN']
    }
    post('https://slack.com/api/reactions.add', arguments)

def react():
    if request.json['event']['type'] == 'message':
        _message()
    elif request.json['event']['type'] == 'reaction_added':
        return _reaction()
    return False

def _reaction():
    if request.json['event']['reaction'] == environ['REACTION']:
        _react(request.json['event']['item']['channel'], request.json['event']['item']['ts'])
        return True
    return False