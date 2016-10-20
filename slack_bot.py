import os
import sys
import re
import getopt
from time import sleep
from slackclient import SlackClient


class SlackBot(object):
    READ_WEBSOCKET_DELAY = 1

    def __init__(self):
        """Constructor"""
        self.client = None
        self.bot_id = os.environ.get("BOT_ID")
        self.__at_bot = "<@{}>".format(self.bot_id)
        self.__channel_id = None
        self.__user_id = None

    def connect(self):
        """Connect to the real time message client """
        self.client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        if self.client.rtm_connect():
            pass
        else:
            print("Connection failed. Invalid Slack token or bot ID?")

    def __parse_slack_output(self, slack_rtm_output):
        """Parses the Slack output and triggers on commands explicitly addressed to the bot"""
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.__at_bot in output['text']:
                    # Return text after @ mention and remove whitespace
                    return output['text'].split(self.__at_bot)[1].strip().lower(), output['channel'], output['user']
        return None, None, None

    def run(self):
        """Infinite loop that listens to Slack"""
        while True:
            try:
                command, self.__channel_id, self.__user_id = self.__parse_slack_output(self.client.rtm_read())
                if command and self.__channel_id and self.__user_id:
                    self.__handle_command(command)
                sleep(self.READ_WEBSOCKET_DELAY)
            except Exception as e:
                print("Exception: ", e.message)

    def __post(self, message):
        """Post a message in the active channel"""
        channel = self.client.server.channels.find(self.__channel_id)
        if not channel:
            raise Exception("Channel {} not found.".format(self.__channel_id))
        return channel.send_message(message)

    def _raise_exception_post(self, message):
        """Raises an exception message in the Slack client"""
        self.__post('Exception thrown with message: {}'.format(message))

    def __handle_command(self, command):
        """Process entered message"""
        user = self.client.server.users.find(self.__user_id)
        username = user.name
        if 'exit' in command:
            sys.exit()
        if 'deploy' in command:
            # Parse parameters
            args = command.split('deploy')[1].split()
            opts, args = getopt.getopt(args, 'h:u:', ['host=', 'update='])
            update = False
            host = None
            for o, a in opts:
                if o in ('-h', '--host'):
                    host = a
                    if 'prod' in host:
                        host = 'remote_prod'
                    elif 'test' in host:
                        host = 'remote_test'
                    else:
                        m = re.match('([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})', host)
                        if m is None:
                            exception_message = "Invalid host parameter '{}'".format(host)
                            self._raise_exception_post(exception_message)
                            return
                        else:
                            host = m.group(0)
                if o in ('-u', '--update'):
                    update = a
                    if update in ('true', 'false'):
                        update = a == 'true'
                    else:
                        exception_message = "Invalid update parameter '{}'".format(update)
                        self._raise_exception_post(exception_message)
                        return

            response = 'User {} wants to deploy on {} host and wants to update the Docker base image'\
                .format(username, host)
            if not update:
                response = 'User {} wants to deploy on {} host but does not want to update the Docker base image' \
                    .format(username, host)

            self.__post(response)


if __name__ == "__main__":
    bot = SlackBot()
    bot.connect()
    bot.run()