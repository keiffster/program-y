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

import logging
import time
import os
import tweepy
from tweepy.error import RateLimitError

from programy.clients.client import BotClient
from programy.config.sections.client.twitter import TwitterConfiguration

class TwitterBotClient(BotClient):

    FIFTEEN_MINUTES = 15*60

    def __init__(self, argument_parser=None):
        self._username = "unknown"
        self._username_len = 0
        self._welcome_message = None
        self._api = None
        BotClient.__init__(self, "Twitter", argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Twitter")

    def get_client_configuration(self):
        return TwitterConfiguration()

    def _get_username(self, bot):
        self._username = bot.license_keys.get_key("TWITTER_USERNAME")
        self._username_len = len(self._username) # Going to get used quite a lot

    def _get_consumer_secrets(self, bot):
        consumer_key = bot.license_keys.get_key("TWITTER_CONSUMER_KEY")
        consumer_secret = bot.license_keys.get_key("TWITTER_CONSUMER_SECRET")
        return consumer_key, consumer_secret

    def _get_access_secrets(self, bot):
        access_token = bot.license_keys.get_key("TWITTER_ACCESS_TOKEN")
        access_token_secret = bot.license_keys.get_key("TWITTER_ACCESS_TOKEN_SECRET")
        return access_token, access_token_secret

    def _create_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def _initialise(self):
        self._welcome_message = self.configuration.client_configuration.welcome_message
        self._get_username(self.bot)
        consumer_key, consumer_secret = self._get_consumer_secrets(self.bot)
        access_token, access_token_secret = self._get_access_secrets(self.bot)
        self._api = self._create_api(consumer_key, consumer_secret, access_token, access_token_secret)

    #############################################################################################
    # Direct Messages

    def _get_direct_messages(self, last_message_id):
        if last_message_id == -1:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Getting latest direct messages")
            messages = self._api.direct_messages()
        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Getting latest direct messages since : %s", last_message_id)
            messages = self._api.direct_messages(since_id=last_message_id)
        messages.sort(key=lambda msg: msg.id)
        return messages

    def _process_direct_message_question(self, userid, text):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Direct Messages: %s -> %s", userid, text)
        response = self.bot.ask_question(userid, text, responselogger=self)
        self._api.send_direct_message(userid, text=response)

    def _process_direct_messages(self, last_message_id):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Processing direct messages since [%s]", last_message_id)

        messages = self._get_direct_messages(last_message_id)

        for message in messages:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("message: %s", message.text)
            try:
                self._process_direct_message_question(message.sender_id, message.text)
            except Exception as err:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error(err)

        if messages:
            last_message_id = messages[-1].id

        return last_message_id

    #############################################################################################
    # Followers

    def _unfollow_non_followers(self, friends, followers_ids):
        for friend_id in friends:
            if friend_id not in followers_ids:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Removing previous friendship with [%d]", friend_id)
                self._api.destroy_friendship(friend_id)

    def _follow_new_followers(self, followers, friends):
        for follower in followers:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Checking follower [%s]", follower.screen_name)
            if follower.id not in friends:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Following %s", follower.screen_name)
                follower.follow()
                self._api.send_direct_message(follower.id, text=self._welcome_message)

    def _process_followers(self):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Processing followers")
        followers = self._api.followers()
        followers_ids = [x.id for x in followers]
        friends = self._api.friends_ids()

        # Unfollow anyone I follow that does not follow me
        self._unfollow_non_followers(friends, followers_ids)

        # Next follow those new fellows following me
        self._follow_new_followers(followers, friends)

    #############################################################################################
    # Status (Tweets)

    def _get_statuses(self, last_status_id):
        if last_status_id == -1:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Getting latest statuses")
            statuses = self._api.home_timeline()
        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Getting latest statuses since : %s", last_status_id)

            statuses = self._api.home_timeline(since_id=last_status_id)

        statuses.sort(key=lambda msg: msg.id)
        return statuses

    def _get_question_from_text(self, text):
        if '@' not in text:
            return None

        text = text.strip()
        pos = text.find(self._username)
        if pos == -1:
            return None

        pos = pos - 1   # Take into account @ sign
        question = text[(pos+self._username_len)+1:]
        return question.strip()

    def _process_status_question(self, userid, text):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Status Update: %s -> %s", userid, text)

        question = self._get_question_from_text(text)
        if question is not None:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("%s -> %s", userid, question)

            response = self.bot.ask_question(userid, question, responselogger=self)

            user = self._api.get_user(userid)
            status = "@%s %s"%(user.screen_name, response)

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(status)

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Sending status response [@%s] [%s]",user.screen_name, response)

            self._api.update_status(status)

    def _process_statuses(self, last_status_id):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Processing status updates since [%s]", last_status_id)

        statuses = self._get_statuses(last_status_id)

        for status in statuses:

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("%s Received Status From[%s] - To[%s] -> [%s]", status.id, status.author.screen_name, self._username, status.text)

            if status.author.screen_name != self._username:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("status: %s", status.text)
                try:
                    self._process_status_question(status.user.id, status.text)
                except Exception as err:
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error(err)

            last_status_id = status.id

        return last_status_id

    #############################################################################################
    # Message ID Storage

    def _get_last_message_ids(self):
        last_direct_message_id = -1
        last_status_id = -1

        if self.configuration.client_configuration.storage == 'file':
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Reads messages ids from [%s]", self.configuration.client_configuration.storage_location)
            if os.path.exists(self.configuration.client_configuration.storage_location):
                try:
                    with open(self.configuration.client_configuration.storage_location, "r", encoding="utf-8") as idfile:
                        last_direct_message_id = int(idfile.readline().strip())
                        last_status_id = int(idfile.readline().strip())
                except Exception as excep:
                    logging.exception(excep)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug ("Got Last Messaged ID: %s", last_direct_message_id)
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug ("Got Last Status ID: %s", last_status_id)

        return (last_direct_message_id, last_status_id)

    def _store_last_message_ids(self, last_direct_message_id, last_status_id):
        if self.configuration.client_configuration.storage == 'file':
            try:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Storing Last Messaged ID: %s", last_direct_message_id)

                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Storing Last Status ID: %s", last_status_id)

                with open(self.configuration.client_configuration.storage_location, "w+", encoding="utf-8") as idfile:
                    idfile.write("%d\n"%last_direct_message_id)
                    idfile.write("%d\n"%last_status_id)

            except Exception as excep:
                logging.exception(excep)

    #############################################################################################
    # Execution

    def _poll(self, last_direct_message_id, last_status_id):
        if self.configuration.client_configuration.use_direct_message is True:
            if self.configuration.client_configuration.auto_follow is True:
                self._process_followers()

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Processing direct messaages")

            last_direct_message_id = self._process_direct_messages(last_direct_message_id)

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Last message id = %d", last_direct_message_id)

        if self.configuration.client_configuration.use_status is True:

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Processing status messaages")

            last_status_id = self._process_statuses(last_status_id)

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Last status id = %d", last_status_id)

        self._store_last_message_ids(last_direct_message_id, last_status_id)

        time.sleep(self.configuration.client_configuration.polling_interval)

    def _use_polling(self):

        print("Twitter client running as [%s]..."%self._username)

        running = True
        while running is True:
            try:
                (last_direct_message_id, last_status_id) = self._get_last_message_ids()

                self._poll(last_direct_message_id, last_status_id)

            except KeyboardInterrupt:
                running = False

            except RateLimitError:

                if self.configuration.client_configuration.rate_limit_sleep != -1:
                    rate_limit_sleep = self.configuration.client_configuration.rate_limit_sleep
                else:
                    rate_limit_sleep = self.FIFTEEN_MINUTES

                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("Rate limit exceeded, sleeping for %d seconds", rate_limit_sleep)

                time.sleep(rate_limit_sleep)

            except Exception as excep:
                logging.exception(excep)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Exiting gracefully...")

    def _use_streaming(self):
        raise NotImplementedError("Streaming currently not supported in this release")

    def run(self):

        self._initialise()

        if self.configuration.client_configuration.polling is True:
            self._use_polling()
        elif self.configuration.client_configuration.streaming is True:
            self._use_streaming()
        else:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("No Twitter interactiong model specified in config ( polling or streaming )")

if __name__ == '__main__':

    def run():
        print("Loading Twitter client, please wait. See log output for progres...")
        twitter_app = TwitterBotClient()
        twitter_app.run()

    run()
