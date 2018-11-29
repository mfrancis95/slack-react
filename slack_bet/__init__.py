from slack_bet.slack import get_channel, react
from flask import abort, Flask, jsonify, request
from os import environ
from slack_bet.database import get_top_reactions, insert_reaction

_get_channels = lambda channels : sorted(get_channel(channel) for channel in channels)
_join_channels = lambda channels : ', '.join(f'*#{channel}*' for channel in _get_channels(channels))

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    if request.json.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    if request.json['type'] == 'url_verification':
        return request.json['challenge']
    if react() and request.json['event']['item']['channel'][0] == 'C':
        insert_reaction(request.json['event']['item']['channel'], request.json['event']['item_user'], request.json['event']['item']['ts'])
    return ''

@app.route('/' + environ['REACTION'], methods = ['POST'])
def statistics():
    if request.form.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    top = request.form.get('text', '')
    if top == 'today':
        text = 'today'
    elif top == 'month':
        text = 'of the month'
    elif top == 'week':
        text = 'of the week'
    elif top == 'year':
        text = 'of the year'
    else:
        text = 'of all-time'
    text = f'Top # of :{environ["REACTION"]}:s {text}:\n'
    for index, reactions in enumerate(get_top_reactions(top), 1):
        text += f'{index}. {_join_channels(reactions["channels"])} - {reactions["_id"]}\n'
    return jsonify(response_type = 'in_channel', text = text)