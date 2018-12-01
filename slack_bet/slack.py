from re import compile, I
from os import environ
from requests import get, post
from flask import request

get_name = lambda field, id: _get_channel(id) if field == 'channel' else _get_user_name(id)
_regex = compile(environ['REGEX'], I)

def _get_channel(channel):
    return '#' + get('https://slack.com/api/channels.info', {
        'channel': channel,
        'token': environ['OAUTH_TOKEN']
    }).json()['channel']['name']

def _get_user_name(user):
    return get('https://slack.com/api/users.info', {
        'token': environ['OAUTH_TOKEN'],
        'user': user
    }).json()['user']['profile']['display_name']

def _message():
    try:
        if _regex.search(request.json['event']['text']):
            _react(request.json['event']['channel'], request.json['event']['ts'])
    except:
        pass

def _react(channel, timestamp):
    post('https://slack.com/api/reactions.add', {
        'channel': channel,
        'name': environ['REACTION'],
        'timestamp': timestamp,
        'token': environ['OAUTH_TOKEN']
    })

def react():
    if request.json['event']['type'] == 'message':
        _message()
    elif request.json['event']['type'] == 'reaction_added':
        return _reaction()
    return False

def _reaction():
    if request.json['event']['reaction'] != environ['REACTION']:
        return False
    _react(request.json['event']['item']['channel'], request.json['event']['item']['ts'])
    return True