import os
from flask import Flask, request, Response
import json


app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/', methods=['POST'])
def toto():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = '{} in {} says {}'.format(username, channel, text)
        print(inbound_message)
        js = json.dumps({"text": "Coucou depuis le webhook!"})
        resp = Response(js, status=200, mimetype='application/json')
    else:
        js = json.dumps({"text": "Bad request!"})
        resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    # Use ngrok for easy and secure tunneling to localhost
    # First launch ngrok with the command:
    # > ngrok http 5000
    # This command will initiate a tunneling to localhost:5000
    # Set the Slack application webhook URL to the given ngrok URL
    # Set the SLACK_WEBHOOK_SECRET environment variable in the config of the python script on pycharm
    # Enjoy!
    app.run(debug=True)