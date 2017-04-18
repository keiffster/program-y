import fbchat
import logging
import time

from programy.clients.clients import BotClient
from programy.config.client.facebook import FacebookClientConfiguration

class FacebookStreamingClient(fbchat.Client):

    def __init__(self, botclient, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self._bot_client = botclient

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)

        if str(author_id) != str(self.uid):
            self._bot_client.process_message(author_id, message)


class FacebookBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)
        self._client = None

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Facebook"])

    def get_client_configuration(self):
        return FacebookClientConfiguration()

    def _initialise(self):
        self._username = self.bot.brain.license_keys.get_key("FACEBOOK_USERNAME")
        self._password = self.bot.brain.license_keys.get_key("FACEBOOK_PASSWORD")

    def use_polling(self):
        logging.debug("Running Facebook using polling model")
        self._client = fbchat.Client(self._username, self._password)

        running = True
        while running is True:
            try:
                author_id = None
                message = None

                self.process_message(author_id, message)

                time.sleep(self.configuration.twitter_configuration.polling_interval)

            except KeyboardInterrupt:
                running = False

            except Exception as e:
                logging.exception(e)

        logging.debug("Exiting gracefully...")

    def process_message(self, author_id, message):
        logging.debug("%s -> %s"%(author_id, message))
        response = self.bot.ask_question(author_id, message)
        logging.debug(response)
        self._client.send(author_id, response)

    def use_streaming(self):
        logging.debug("Running Facebook using streaming model")
        self._client = FacebookStreamingClient(self, self._username, self._password)
        logging.debug("Listening...")
        self._client.listen()

    def run(self):
        self._initialise()

        if self.configuration.facebook_configuration.polling is True:
            self.use_polling()
        elif self.configuration.facebook_configuration.streaming is True:
            self.use_streaming()
        else:
            logging.error("No Facebook interactiong model specified in config ( polling or streaming )")


if __name__ == '__main__':

    def run():
        logging.debug("Loading Facebook client, please wait...")
        facebook_app = FacebookBotClient()
        facebook_app.run()

    run()

