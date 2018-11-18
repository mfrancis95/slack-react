from flask import abort, Flask, jsonify, request
from os import environ
from slack_bet.slack import get_channel, react
from slack_bet.database import bet, get_top_bets

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    if request.json.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    if request.json['type'] == 'url_verification':
        return request.json['challenge']
    if react() and request.json['event']['item']['channel'][0] == 'C':
        bet(request.json['event']['item']['channel'], request.json['event']['item']['ts'])
    return ''

@app.route('/' + environ['REACTION'], methods = ['POST'])
def statistics():
    if request.form.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    text = f'Top # of :{environ["REACTION"]}:s today:\n'
    for index, bets in enumerate(get_top_bets(), 1):
        text += f'{index}. *#{get_channel(bets["_id"])}* - {bets["count"]}\n'
    return jsonify({'response_type': 'in_channel', 'text': text})