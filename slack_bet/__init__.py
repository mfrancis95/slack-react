from flask import Flask, jsonify, request
from re import IGNORECASE, match, search
from os import environ
from requests import post

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    if request.json['type'] == 'url_verification':
        return request.json['challenge']
    try:
        if match('bet$', request.json['event']['text'], IGNORECASE) or search(':bet:', request.json['event']['text'], IGNORECASE):
            arguments = {
                'channel': request.json['event']['channel'],
                'name': 'bet',
                'timestamp': request.json['event']['ts'],
                'token': environ['OAUTH_TOKEN']
            }
            post('https://slack.com/api/reactions.add', arguments)
    except:
        pass
    return ''