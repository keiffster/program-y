"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import time
import datetime
import tweepy
from tweepy.error import RateLimitError
from programy.utils.logging.ylogger import YLogger
from programy.clients.polling.client import PollingBotClient
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.utils.console.console import outputLog


class TwitterListener(tweepy.StreamListener):

    def __init__(self, twitter_bot_client):
        self._twitter_bot_client = twitter_bot_client
        self.api = twitter_app._api

    def on_status(self, status):
        self._twitter_bot_client.handle_mention(status)

    def on_error(self, status):
        YLogger.error(self, status)


class TwitterBotClient(PollingBotClient):
    FIFTEEN_MINUTES = 15 * 60

    def __init__(self, argument_parser=None):
        self._username = "unknown"
        self._username_len = 0
        self._welcome_message = None
        self._api = None
        self._me = None
        self._consumer_key = None
        self._consumer_secret = None
        self._access_token = None
        self._access_token_secret = None

        self._direct_id = -1

        PollingBotClient.__init__(self, "twitter", argument_parser)

    def get_client_configuration(self):
        return TwitterConfiguration()

    def get_license_keys(self):
        self._username = self.license_keys.get_key("TWITTER_USERNAME")
        self._consumer_key = self.license_keys.get_key("TWITTER_CONSUMER_KEY")
        self._consumer_secret = self.license_keys.get_key("TWITTER_CONSUMER_SECRET")
        self._access_token = self.license_keys.get_key("TWITTER_ACCESS_TOKEN")
        self._access_token_secret = self.license_keys.get_key("TWITTER_ACCESS_TOKEN_SECRET")
        self._username_len = len(self._username)  # Going to get used quite a lot

    def _create_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)
        try:
            api.verify_credentials()
            return api

        except Exception as error:
            YLogger.exception(self, "Error creating api", error)
            return None

    def connect(self):
        if self._consumer_key is not None and \
                self._consumer_secret is not None and \
                self._access_token is not None and \
                self._access_token_secret is not None:
            self._welcome_message = self.configuration.client_configuration.welcome_message
            self._api = self._create_api(self._consumer_key,
                                         self._consumer_secret,
                                         self._access_token,
                                         self._access_token_secret)
            self._me = self._api.me()
            return True

        return False

    def display_connected_message(self):
        outputLog(self, "Twitter Bot connected and running...")

    def ask_question(self, userid, question):
        self._questions += 1
        client_context = self.create_client_context(userid)
        return client_context.bot.ask_question(client_context, question, responselogger=self)

    def _follow_followers(self):
        YLogger.debug(self, "Retrieving and following followers")
        for follower in tweepy.Cursor(self._api.followers).items():
            if not follower.following:
                YLogger.debug(self, f"Following {follower.name}")
                follower.follow()

    def handle_mention(self, tweet):
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self._me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return

        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()

            except Exception as e:
                YLogger.error("Error on fav", exc_info=True)

        # Reply to the user
        try:
            author = tweet.author.screen_name

            question = " ".join(tweet.text.split(" ")[1:])
            YLogger.debug(self, "Mention: %s", question)

            response = self.ask_question(author, question)

            reply = "@{0} {1}".format(author, response)
            YLogger.debug(self, "Mention reply: %s", reply)

            self._api.update_status(reply, in_reply_to_status_id=tweet.id)

        except Exception as error:
            YLogger.exception(self, "Error handling mention", error)

    def _check_directs(self):
        try:
            YLogger.info(self, "Retrieving directs")
            new_since_id = self._direct_id
            if self._direct_id == -1:
                tweets = tweepy.Cursor(self._api.list_direct_messages).items()
            else:
                tweepy.Cursor(self._api.list_direct_messages, count=10, cursor=new_since_id).items()

            for tweet in tweets:
                new_since_id = max(tweet.id, new_since_id)

            self._direct_id = new_since_id

        except Exception as error:
            YLogger.exception(self, "Failure handling direct", error)

    def pre_poll(self):
        if self.configuration.client_configuration.respond_to_mentions is True:
            YLogger.debug(self, "Responding to mentions: %s", self.configuration.client_configuration.mentions)
            stream = tweepy.Stream(self._api.auth, TwitterListener(self))
            stream.filter(track=self.configuration.client_configuration.mentions, languages=["en"], is_async=True)

    def poll_and_answer(self):

        running = True
        sleepy_time = self._configuration.client_configuration.polling_interval

        try:
            if self._configuration.client_configuration.follow_followers is True:
                YLogger.debug(self, "Following followers")
                self._follow_followers()

            if self._configuration.client_configuration.respond_to_directs:
                YLogger.debug(self, "Checking direct messages")
                self._check_directs()

            YLogger.debug(self, "Sleeping for %d at %s" %(sleepy_time, datetime.datetime.now().strftime("%H:%M:%S")))

        except KeyboardInterrupt:
            running = False

        except RateLimitError:

            outputLog(self, "Rate limit exceeded, check logs!")
            YLogger.error(self, "Rate limit exceeded, sleeping for %d seconds", self._rate_limit_sleep)

            sleepy_time = self._rate_limit_sleep

        except Exception as excep:
            YLogger.exception(self, "Poll and answer error", excep)

        time.sleep(sleepy_time)

        return running


if __name__ == '__main__':
    outputLog(None, "Initiating Twitter Client...")

    twitter_app = TwitterBotClient()
    twitter_app.run()
