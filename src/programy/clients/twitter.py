import logging
import tweepy
from tweepy.error import RateLimitError
import time
import os

from programy.clients.clients import BotClient
from programy.config.client.twitter import TwitterClientConfiguration

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print(status.text)
        pass

class TwitterBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Twitter"])

    def get_client_configuration(self):
        return TwitterClientConfiguration()

    def process_direct_messages(self, last_message_id):
        logging.debug ("Processing direct messages since [%s]"%last_message_id)

        if last_message_id == -1:
            logging.debug("Getting latest direct messages")
            messages = self._api.direct_messages()
        else:
            logging.debug("Getting latest direct messages since : %s" % last_message_id)
            messages = self._api.direct_messages(since_id=last_message_id)
        messages.sort(key=lambda msg: msg.id)

        for message in messages:
            logging.debug("message: %s"% message.text)
            try:
                self.process_direct_message_question(message.sender_id, message.text)
            except Exception as err:
                logging.error(err)

        if len(messages) > 0:
            last_message_id = messages[-1].id

        return last_message_id

    def process_followers(self):
        logging.debug("Processing followers")
        followers = self._api.followers()
        followers_ids = [x.id for x in followers]
        friends = self._api.friends_ids()

        # Unfollow anyone I follow that does not follow me
        for friend_id in friends:
            if friend_id not in followers_ids:
                logging.debug ("Removing previous friendship with [%d]"%(friend_id))
                self._api.destroy_friendship(friend_id)

        # Next follow those new fellows following me
        for follower in followers:
            logging.debug ("Checking follower [%s]"%follower.screen_name)
            if follower.id not in friends:
                logging.debug("Following %s"%follower.screen_name)
                follower.follow()
                self._api.send_direct_message(follower.id, text=self._welcome_message)

    def process_direct_message_question(self, userid, text):
        logging.debug("Direct Messages: %s -> %s"%(userid, text))
        response = self.bot.ask_question(userid, text)
        self._api.send_direct_message(userid, text=response)

    def process_statuses(self, last_status_id):
        logging.debug ("Processing status updates since [%s]"%last_status_id)

        if last_status_id == -1:
            logging.debug("Getting latest statuses")
            statuses = self._api.home_timeline()
        else:
            logging.debug("Getting latest statuses since : %s" % last_status_id)
            statuses = self._api.home_timeline(since_id=last_status_id)
            statuses.sort(key=lambda msg: msg.id)

        for status in statuses:
            print ("[%s] - [%s]"%(status.author.screen_name, self._username))
            if status.author.screen_name != self._username:
                logging.debug("status: %s" % status.text)
                try:
                    self.process_status_question(status.user.id, status.text)
                except Exception as err:
                    logging.error(err)

        if len(statuses) > 0:
            last_status_id = statuses[-1].id

        return last_status_id

    def process_status_question(self, userid, text):
        logging.debug("Status Update: %s -> %s"%(userid, text))

        text = text.strip()
        pos = text.find(self._username)
        if pos == -1:
            return
        pos = pos - 1   # Take into account @ sign

        question = text[(pos+self._username_len)+1:]

        logging.debug("%s -> %s"%(userid, question))

        response = self.bot.ask_question(userid, question)

        user = self._api.get_user(userid)
        status = "@%s %s"%(user.screen_name, response)

        logging.debug(status)
        self._api.update_status(status)

    def initialise(self):
        consumer_key = self.bot.license_keys.get_key("TWITTER_CONSUMER_KEY")
        consumer_secret = self.bot.license_keys.get_key("TWITTER_CONSUMER_SECRET")

        access_token = self.bot.license_keys.get_key("TWITTER_ACCESS_TOKEN")
        access_token_secret = self.bot.license_keys.get_key("TWITTER_ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._welcome_message = self.configuration.twitter_configuration.welcome_message

        self._api = tweepy.API(auth)

        self._username = self.bot.license_keys.get_key("TWITTER_USERNAME")
        self._username_len = len(self._username) # Going to get used quite a lot

    def get_last_message_ids(self):
        last_direct_message_id = -1
        last_status_id = -1

        if self.configuration.twitter_configuration.storage == 'file':
            logging.debug("Reads messages ids from [%s]" % self.configuration.twitter_configuration.storage_location)
            if os.path.exists(self.configuration.twitter_configuration.storage_location):
                try:
                    with open(self.configuration.twitter_configuration.storage_location, "r+") as idfile:
                        last_direct_message_id = int(idfile.readline().strip())
                        last_status_id = int(idfile.readline().strip())
                except Exception as e:
                    logging.exception(e)

        return (last_direct_message_id, last_status_id)

    def store_last_message_ids(self, last_direct_message_id, last_status_id):
        if self.configuration.twitter_configuration.storage == 'file':
            logging.debug("Writing messages ids to [%s]" % self.configuration.twitter_configuration.storage_location)
            try:
                with open(self.configuration.twitter_configuration.storage_location, "w+") as idfile:
                    idfile.write("%d\n"%last_direct_message_id)
                    idfile.write("%d\n"%last_status_id)
            except Exception as e:
                logging.exception(e)

    def use_polling(self):

        (last_direct_message_id, last_status_id) = self.get_last_message_ids()

        running = True
        while running is True:
            try:
                if self.configuration.twitter_configuration.use_direct_message is True:
                    if self.configuration.twitter_configuration.auto_follow is True:
                        self.process_followers()

                    last_direct_message_id = self.process_direct_messages(last_direct_message_id)
                    logging.debug("Last message id = %d"% last_direct_message_id)

                if self.configuration.twitter_configuration._use_status is True:
                    last_status_id = self.process_statuses(last_status_id)
                    logging.debug("Last status id = %d"% last_status_id)

                self.store_last_message_ids(last_direct_message_id, last_status_id)

                time.sleep(self.configuration.twitter_configuration.polling_interval)

            except KeyboardInterrupt:
                running = False

            except RateLimitError as re:
                logging.error("Rate limit exceeded, sleeping for 15 minutes")
                time.sleep(15*60)

            except Exception as e:
                logging.exception(e)

        logging.debug("Exiting gracefully...")

    def use_streaming(self):
        pass

    def run(self):

        self.initialise()

        if self.configuration.twitter_configuration.polling is True:
            self.use_polling()
        elif self.configuration.twitter_configuration.streaming is True:
            self.use_streaming()
        else:
            logging.error("No Twitter interactiong model specified in config ( polling or streaming )")

if __name__ == '__main__':

    def run():
        print("Loading Twitter client, please wait. See log output for progres...")
        twitter_app = TwitterBotClient()
        twitter_app.run()

    run()