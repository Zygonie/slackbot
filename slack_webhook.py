import os
from flask import Flask, request, Response


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
    return Response(), 200


if __name__ == "__main__":
    # Use ngrok for easy and secure tunneling to localhost
    app.run(debug=True)