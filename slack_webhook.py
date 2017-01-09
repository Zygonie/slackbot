#*************************************************************************************************************
#
# Use ngrok for easy and secure tunneling to localhost
# First launch ngrok with the command:
# > ngrok http 5000
# This command will initiate a tunneling to localhost:5000
# Set the Slack application webhook URL to the given ngrok URL
# Set the SLACK_WEBHOOK_SECRET environment variable in the config of the python script on pycharm
# Enjoy!
#
#*************************************************************************************************************

import os
from flask import Flask, request, Response, render_template
from flask_socketio import SocketIO, emit, send
import json

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #os.environ.get('WEBHOOK_APP_SECRET')
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/webhook', methods=['POST'])
def webhook():
    """On utilise un `bot` dans Slack qui, lorsqu'on entre le mot clef `deploy` pour commencer une ligne, Slack
     va alors effectuer un POST vers l'URL qu'on lui donnne (celle de ngrok). On recupere alors le contenu du POST
     ici et on l'affiche en temps reel avec les WebSockets sur une page HTML. De meme, on retourne une reponse a
     Slack qui affiche son contenu.
     D'apres la doc (https://api.slack.com/outgoing-webhooks):
     If the handler wishes to post a response back into the channel, the following JSON should be returned as the body
     of the response:
     {
       "text": "African or European?"
     }
     Empty bodies or bodies with an empty text property will simply be ignored.
     Non-200 responses will be retried a reasonable number of times.
     Responses will be posted using the bot name and icon configured in the integration. However, if you would like to
     change the name on a per-response basis, simply include the username parameter in your response."""
    global sid
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        websocket_inbound_message = '{} in {} says {}'.format(username, channel, text)
        response_to_slack = "Request from {} with message \n\n*'{}'*\n\n has well been received".format(username, text)
        js = json.dumps({"text": response_to_slack})
        resp = Response(js, status=200, mimetype='application/json')
        emit('server_message_ready', {'data': websocket_inbound_message}, namespace='/slack', broadcast=True)
    else:
        js = json.dumps({"text": "Bad request!"})
        resp = Response(js, status=200, mimetype='application/json')
        emit('server_message_ready', {'data': 'Unknown token'}, namespace='/slack', broadcast=True)
    return resp


@socketio.on('connect', namespace='/slack')
def on_connect():
    global sid
    sid = request.sid
    emit('server_message_ready', {'data': 'Connected'})


@socketio.on('client_message_ready', namespace='/slack')
def on_client_message_ready(json):
    print('Received json: ' + str(json))

if __name__ == "__main__":
    # Use ngrok for easy and secure tunneling to localhost
    # First launch ngrok with the command:
    # > ngrok http 5000
    # This command will initiate a tunneling to localhost:5000
    # Set the Slack application webhook URL to the given ngrok URL
    # Set the SLACK_WEBHOOK_SECRET environment variable in the config of the python script on pycharm
    # Enjoy!
    socketio.run(app, debug=True)
    #TODO: Add support to storing posts to a mongodb database with pymongo (no ORM)
    #TODO: Deploy to heroku
