"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import logging
import time
import re

from slackclient import SlackClient

from programy.clients.client import BotClient
from programy.config.sections.client.slack_client import SlackConfiguration


SLACK_CLIENT = None


class SlackBotClient(BotClient):

    # constants
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "slack", argument_parser)

        self.get_token()

        self._polling_interval = self.configuration.client_configuration.polling_interval

        self._slack_client = self.create_slack_client()

        self._running = True

    def set_environment(self):
        self.bot.brain.properties.add_property("env", 'Slack')

    def get_client_configuration(self):
        return SlackConfiguration()

    def get_token(self,):
         self._bot_token = self.bot.license_keys.get_key("SLACK_TOKEN")

    def create_slack_client(self):
        return SlackClient(self._bot_token)

    def connect_to_slack(self):
        return self._slack_client.rtm_connect(with_team_state=False)

    def get_bot_id(self):
        return self._slack_client.api_call("auth.test")["user_id"]

    def parse_bot_messages(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot messages.
            If a bot message is found, this function returns a tuple of message and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                text = event["text"]

                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Slack received [%s] "%text)

                user_id, message = self.parse_direct_mention(text)

                if user_id == self._starterbot_id:
                    return message, event["channel"], event['user']

        return None, None, None


    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def ask_question(self, sessionid, question):
        response = self.bot.ask_question(sessionid, question, responselogger=self)
        return response

    def handle_message(self, message, channel, user_id):

        # Finds and executes the given message, filling in response
        response = self.ask_question(user_id, message)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Slack sending [%s] to [%s]" % (message, user_id))

        # Sends the response back to the channel
        self._slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or response
        )

    def run(self):

        if self.connect_to_slack():
            print("Starter Bot connected and running!")

            # Read bot's user ID by calling Web API method `auth.test`
            self._starterbot_id = self.get_bot_id()

            while self._running:
                try:
                    message, channel, user_id = self.parse_bot_messages(self._slack_client.rtm_read())
                    if message:
                        self.handle_message(message, channel, user_id)
                    time.sleep(self._polling_interval)
                except KeyboardInterrupt:
                    self._running = False
                except Exception as excep:
                    logging.exception(excep)

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Exiting gracefully...")

        else:
            print("Connection failed. Exception traceback printed above.")


if __name__ == '__main__':

    print("Loading Slack client, please wait. See log output for progress...")
    SLACK_CLIENT = SlackBotClient()
    SLACK_CLIENT.run()


