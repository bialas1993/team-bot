import os
import slack
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN=os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=SLACK_TOKEN)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/users')
@cross_origin()
def users():
    request = client.api_call("users.list")
    if request['ok']:
        return jsonify(request['members'])
    return make_response(jsonify({'error': 'Can not find users'}), 400)

@app.route('/channels')
@cross_origin()
def channels():
    request = client.api_call("conversations.list")
    if request['ok']:
        return jsonify(request['channels'])
    return make_response(jsonify({'error': 'Can not find channels'}), 400)

@app.route('/channels/<channel>/users')
@cross_origin()
def channel_users(channel):
    request = client.api_call("conversations.members", params={'channel': channel})
    if request['ok']:
        users = []
        for _, member in enumerate(request['members']):
            req = client.api_call("users.info", params={'user': member})
            users.append(req['user'])

        return jsonify(users)
    return make_response(jsonify({'error': 'Can not find users'}), 400)

if __name__ == '__main__':
    app.run(debug=True)