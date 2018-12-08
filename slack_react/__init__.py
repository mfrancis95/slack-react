from slack_react.slack import get_name, react
from flask import abort, Flask, jsonify, request
from os import environ
from slack_react.database import get_top_reactions, insert_reaction

_get_names = lambda field, ids: sorted(get_name(field, id) for id in ids)
_join_ids = lambda field, ids: ', '.join(f'*{name}*' for name in _get_names(field, ids))

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    if request.json.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    if request.json['type'] == 'url_verification':
        return request.json['challenge']
    if react(request.json['event']) and request.json['event']['item']['channel'][0] == 'C' and 'item_user' in request.json['event']:
        insert_reaction(request.json['event']['item']['channel'], request.json['event']['item_user'], request.json['event']['item']['ts'])
    return ''

@app.route(f'/{environ["REACTION"]}', methods = ['POST'])
def statistics():
    if request.form.get('token') != environ['SLACK_VERIFICATION_TOKEN']:
        abort(403)
    arguments = request.form.get('text', '').split(' ')
    if not len(arguments) or arguments[0] not in ['channels', 'users']:
        return jsonify(response_type = 'ephemeral', text = f'Usage: `/{environ["REACTION"]}` `channels|users` [`month|today|week|year`]')
    field = arguments[0]
    try:
        top = arguments[1]
    except:
        top = ''
    if top == 'today':
        text = 'today'
    elif top == 'month':
        text = 'this month'
    elif top == 'week':
        text = 'this week'
    elif top == 'year':
        text = 'this year'
    else:
        text = 'of all-time'
    text = f'{field.capitalize()} with the most :{environ["REACTION"]}:s {text}:\n'
    field = field[:-1]
    for index, reactions in enumerate(get_top_reactions(field, top), 1):
        text += f'{index}. {_join_ids(field, reactions["ids"])} - {reactions["_id"]}\n'
    return jsonify(response_type = 'in_channel', text = text)