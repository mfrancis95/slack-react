from re import compile, I
from os import environ
from requests import get, post

get_name = lambda field, id: _get_channel(id) if field == 'channel' else _get_user_name(id)
_regex = compile(environ['REGEX'], I)

def _get_channel(channel):
    return f'<#{channel}|' + get('https://slack.com/api/channels.info', {
        'channel': channel, 'token': environ['OAUTH_TOKEN']
    }).json()['channel']['name'] + '>'

def _get_user_name(user):
    return get('https://slack.com/api/users.info', {
        'token': environ['OAUTH_TOKEN'], 'user': user
    }).json()['user']['profile']['display_name']

def _message(event):
    try:
        if _regex.search(event['text']):
            _react(event['channel'], event['ts'])
    except:
        pass

def _react(channel, timestamp):
    post('https://slack.com/api/reactions.add', {
        'channel': channel, 'name': environ['REACTION'], 'timestamp': timestamp,
        'token': environ['OAUTH_TOKEN']
    })

def react(event):
    if event['type'] == 'message':
        _message(event)
    elif event['type'] == 'reaction_added':
        return _reaction(event)
    return False

def _reaction(event):
    if event['reaction'] != environ['REACTION']:
        return False
    _react(event['item']['channel'], event['item']['ts'])
    return True