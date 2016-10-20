# SlackBot
My custom Slack bot for test purpose

You will find examples of the use of Slack API to implement a bot or a webhook.

* Bot can run locally and is like a normal user of the team which can join any channel (also private ones).
* Webhook can also run locally in dev environment with the help of tunneling to localhost (for example with
ngrok). A webhook is an integration into a public Slack channel and is triggered by a chosen word. When this 
word is detected in the message, it is sent to the webhook so that it can be treated server side (a flask app
for example). The command to run the webhook is as follow:
    1- Go to Slack to retrieve the token and export it as SLACK_WEBHOOK_TOKEN environment variable
    2- Run `ngrok http 5000` to tunnel port 5000 (default port of Flask app) to localhost
    3- Copy the public web address, something like `http://d19451bd.ngrok.io/` to the Slack webhook
    4- Enjoy ! For example, type `Hello bot, would you deploy please !` should trigger the webhook