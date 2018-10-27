from flask import Flask, request
from re import IGNORECASE, match, search
from os import environ
from requests import post

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    if request.json['type'] == 'url_verification':
        return request.json['challenge']
    if request.json['event']['type'] == 'message':
        _message()
    elif request.json['event']['type'] == 'reaction_added':
        _reaction()
    return ''

def _message():
    try:
        if match('bet$', request.json['event']['text'], IGNORECASE) or search(':bet:', request.json['event']['text'], IGNORECASE):
            _react(request.json['event']['channel'], request.json['event']['ts'])
    except:
        pass

def _react(channel, timestamp):
    arguments = {
        'channel': channel,
        'name': 'bet',
        'timestamp': timestamp,
        'token': environ['OAUTH_TOKEN']
    }
    post('https://slack.com/api/reactions.add', arguments)

def _reaction():
    if request.json['event']['reaction'] == 'bet':
        _react(request.json['event']['item']['channel'], request.json['event']['item']['ts'])