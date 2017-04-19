"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
from programy.config.base import BaseConfigurationData
from programy.config.client.client import ClientConfiguration

class TwitterConfiguration(BaseConfigurationData):

    def __init__(self):
        self._polling = False
        self._polling_interval = 0
        self._streaming = False
        self._use_status = False
        self._use_direct_message = False
        self._auto_follow = False
        self._storage = None
        self._storage_location = None
        self._welcome_message = "Thanks for following me."
        BaseConfigurationData.__init__(self, "twitter")

    @property
    def polling(self):
        return self._polling

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def streaming(self):
        return self._streaming

    @property
    def use_status(self):
        return self._use_status

    @property
    def use_direct_message(self):
        return self._use_direct_message

    @property
    def auto_follow(self):
        return self._auto_follow

    @property
    def storage(self):
        return self._storage

    @property
    def storage_location(self):
        return self._storage_location

    @property
    def welcome_message(self):
        return self._welcome_message

    def load_config_section(self, config_file, bot_root):
        twitter = config_file.get_section(self.section_name)
        if twitter is not None:
            self._polling = config_file.get_bool_option(twitter, "polling")
            if self._polling is True:
                self._polling_interval = config_file.get_int_option(twitter, "polling_interval")
            self._streaming = config_file.get_bool_option(twitter, "streaming")
            self._use_status = config_file.get_bool_option(twitter, "use_status")
            self._use_direct_message = config_file.get_bool_option(twitter, "use_direct_message")
            if self._use_direct_message is True:
                self._auto_follow = config_file.get_bool_option(twitter, "auto_follow")

            self._storage = config_file.get_option(twitter, "storage")
            if self._storage == 'file':
                storage_loc = config_file.get_option(twitter, "storage_location")
                self._storage_location = self.sub_bot_root(storage_loc, bot_root)

            self._welcome_message = config_file.get_option(twitter, "welcome_message")

class TwitterClientConfiguration(ClientConfiguration):

    def __init__(self):
        ClientConfiguration.__init__(self)
        self._twitter_config = TwitterConfiguration()

    @property
    def twitter_configuration(self):
        return self._twitter_config

    def load_config_data(self, config_file, bot_root):
        super(TwitterClientConfiguration, self).load_config_data(config_file, bot_root)
        self._twitter_config.load_config_section(config_file, bot_root)
