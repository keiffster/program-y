"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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

from programy.utils.logging.ylogger import YLogger
import re

from slackclient import SlackClient

from programy.clients.polling.client import PollingBotClient
from programy.clients.polling.slack.config import SlackConfiguration


SLACK_CLIENT = None


class SlackBotClient(PollingBotClient):

    # constants
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    def __init__(self, argument_parser=None):
        self._bot_token = None

        PollingBotClient.__init__(self, "slack", argument_parser)

        self._slack_client = self.create_client()

    def get_client_configuration(self):
        return SlackConfiguration()

    def parse_configuration(self):
        self._polling_interval = self.configuration.client_configuration.polling_interval

    def get_license_keys(self):
        self._bot_token = self.license_keys.get_key("SLACK_TOKEN")

    def create_client(self):
        return SlackClient(self._bot_token)

    def connect(self):
        if self._slack_client.rtm_connect(with_team_state=False) is True:
            # Read bot's user ID by calling Web API method `auth.test`
            self._starterbot_id = self.get_bot_id()
            return True
        return False

    def get_bot_id(self):
        return self._slack_client.api_call("auth.test")["user_id"]

    def parse_message(self, event):
        text = event["text"]
    
        YLogger.debug(self, "Slack received [%s] ", text)
    
        userid, message = self.parse_direct_mention(text)
    
        if message and userid == self._starterbot_id:
            channel = event['channel']
            self.handle_message(message, channel, userid)

    def parse_messages(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot messages.
            If a bot message is found, this function returns a tuple of message and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                self.parse_message(event)
 
    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        if matches:
            return (matches.group(1), matches.group(2).strip())
        return (None, None)

    def ask_question(self, userid, question):
        self._questions += 1
        client_context = self.create_client_context(userid)
        response = client_context.bot.ask_question(client_context, question, responselogger=self)
        return response

    def send_response(self, response, channel):
        # Sends the response back to the channel
        self._slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or response
        )

    def handle_message(self, message, channel, userid):

        # Finds and executes the given message, filling in response
        response = self.ask_question(userid, message)

        YLogger.debug(self, "Slack sending [%s] to [%s]", message, userid)

        self.send_response(response, channel)

    def get_messages(self):
        return self._slack_client.rtm_read()

    def display_connected_message(self):
        print ("Slack Bot connected and running...")

    def poll_and_answer(self):
        running = True
        try:
            messages = self.get_messages()
            if messages:
                self.parse_messages(messages)
            self.sleep(self._polling_interval)

        except KeyboardInterrupt:
            print("Slack client stopping via keyboard....")
            running = False

        except Exception as excep:
            YLogger.exception(self, "Failed to poll and answer", excep)

        return running


if __name__ == '__main__':

    print("Initiating Slack Client...")

    SLACK_CLIENT = SlackBotClient()
    SLACK_CLIENT.run()
