import logging
import tweepy
import time
import os

from programy.clients.clients import BotClient
from programy.config.client.twitter import TwitterClientConfiguration

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

class TwitterBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Twitter"])

    def get_client_configuration(self):
        return TwitterClientConfiguration()

    def process_direct_messages(self, last_message_id):
        if last_message_id == -1:
            print("Getting latest direct messages")
            messages = self._api.direct_messages()
        else:
            print("Getting latest direct messages since : %s" % last_message_id)
            messages = self._api.direct_messages(since_id=last_message_id)
        messages.sort(key=lambda msg: msg.id)

        for message in messages:
            #print("message: ", message.text)
            try:
                self.process_direct_message_question(api, message.user.id, message.text)
            except Exception as err:
                print(err)

        if len(messages) > 0:
            last_message_id = messages[-1].id

        return last_message_id

    def process_direct_message_question(self, userid, text):
        print("%s -> %s"%(userid, text))
        response = self.bot.ask_question(userid, text)
        self._api.send_direct_message(userid, response)

    def process_statuses(self, last_status_id):
        if last_status_id == -1:
            print("Getting latest statuses")
            statuses = self._api.home_timeline()
        else:
            print("Getting latest statuses since : %s" % last_status_id)
            statuses = self._api.home_timeline(since_id=last_status_id)
            statuses.sort(key=lambda msg: msg.id)

        for status in statuses:
            #print("status: ", status.text)
            try:
                self.process_status_question(api, status.user.id, status.text)
            except Exception as err:
                print(err)

        if len(statuses) > 0:
            last_status_id = statuses[-1].id

        return last_status_id

    def process_status_question(self, userid, text):

        text = text.strip()
        pos = text.find(self._username)
        if pos == -1:
            return

        question = text[(pos+self._username_len+1):]

        print("%s -> %s"%(userid, question))

        response = self.bot.ask_question(userid, question)

        user = self._api.get_user(userid)
        status = "@%s %s"%(user.screen_name, response)

        print (status)
        self._api.update_status(status)

    def initialise(self):
        consumer_key = self.bot.brain.license_keys.get_key("TWITTER_CONSUMER_KEY")
        consumer_secret = self.bot.brain.license_keys.get_key("TWITTER_CONSUMER_SECRET")

        access_token = self.bot.brain.license_keys.get_key("TWITTER_ACCESS_TOKEN")
        access_token_secret = self.bot.brain.license_keys.get_key("TWITTER_ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

        self._username = self.configuration.twitter_configuration.username
        self._username_len = len(self._username) # Going to get used quite a lot

    def get_last_message_ids(self):
        last_direct_message_id = -1
        last_status_id = -1

        if self.configuration.twitter_configuration.storage is 'file':
            if os.path.exists(self.configuration.twitter_configuration.storage_location):
                with open(self.configuration.twitter_configuration.storage_location, "r+") as idfile:
                    last_direct_message_id = idfile.readline()
                    last_status_id = idfile.readline()

        return (last_direct_message_id, last_status_id)

    def store_last_message_ids(self, last_direct_message_id, last_status_id):
        if self.configuration.twitter_configuration.storage is 'file':
            with open(self.configuration.twitter_configuration.storage_location, "w+") as idfile:
                idfile.write(last_direct_message_id + "\n")
                idfile.write(last_status_id + "\n")

    def use_polling(self):

        (last_direct_message_id, last_status_id) = self.get_last_message_ids()

        running = True
        while running is True:
            try:
                if self.configuration.twitter_configuration.use_direct_message is True:
                    last_direct_message_id = self.process_direct_messages(last_direct_message_id)
                    print("Last message id = ", last_direct_message_id)

                if self.configuration.twitter_configuration._use_status is True:
                    last_status_id = self.process_statuses(last_status_id)
                    print("Last status id = ", last_status_id)

                self.store_last_message_ids(last_direct_message_id, last_status_id)

                time.sleep(self.configuration.twitter_configuration.polling_interval)

            except KeyboardInterrupt:
                running = False

        print("Exiting gracefully...")

    def use_streaming(self):
        pass

    def run(self):

        self._initialise()

        if self.configuration.twitter_configuration.polling is True:
            self.use_polling()
        elif self.configuration.twitter_configuration.streaming is True:
            self.use_streaming()
        else:
            logging.error("No Twitter interactiong model specified in config ( polling or streaming )")

if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = TwitterBotClient()
        console_app.run()

    run()