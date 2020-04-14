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
from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class TwitterConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "twitter")
        self._description = 'ProgramY AIML2.0 Twitter Client'
        self._polling_interval = 60
        self._rate_limit_sleep = 900

        self._follow_followers = True
        self._respond_to_mentions = True
        self._respond_to_directs = False

        self._mentions = ['#askprogramy']

        self._welcome_message = "Thanks for following me."

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def rate_limit_sleep(self):
        return self._rate_limit_sleep

    @property
    def follow_followers(self):
        return self._follow_followers

    @property
    def respond_to_mentions(self):
        return self._respond_to_mentions

    @property
    def respond_to_directs(self):
        return self._respond_to_directs

    @property
    def mentions(self):
        return self._mentions

    @property
    def welcome_message(self):
        return self._welcome_message

    def load_configuration_section(self, configuration_file, section, bot_root, subs: Substitutions = None):
        assert section is not None

        self._polling_interval = configuration_file.get_int_option(section, "polling_interval", missing_value=60,
                                                                   subs=subs)
        self._rate_limit_sleep = configuration_file.get_int_option(section, "rate_limit_sleep", missing_value=900,
                                                                   subs=subs)

        self._follow_followers = configuration_file.get_bool_option(section, "follow_followers", missing_value=False,
                                                                   subs=subs)
        self._respond_to_mentions = configuration_file.get_bool_option(section, "respond_to_mentions", missing_value=False,
                                                                   subs=subs)
        self._respond_to_directs = configuration_file.get_bool_option(section, "respond_to_directs", missing_value=True,
                                                                   subs=subs)

        self._mentions = configuration_file.get_multi_option(section, "mentions", missing_value="", subs=subs)

        self._welcome_message = configuration_file.get_option(section, "welcome_message", subs=subs)

        super(TwitterConfiguration, self).load_configuration_section(configuration_file, section, bot_root,
                                                                     subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['polling_interval'] = 60
            data['rate_limit_sleep'] = 900

            data['follow_followers'] = True
            data['respond_to_mentions'] = True
            data['respond_to_directs'] = False

            data['mentions'] = ["#askprogramy"]

            data['welcome_message'] = "Thanks for following me."

            data['storage'] = 'file'
            data['storage_location'] = './storage/twitter.data'

        else:
            data['polling_interval'] = self._polling_interval
            data['rate_limit_sleep'] = self._rate_limit_sleep

            data['follow_followers'] = self._follow_followers
            data['respond_to_mentions'] = self._respond_to_mentions
            data['respond_to_directs'] = self._respond_to_directs

            data['mentions'] = self._mentions[:]

            data['welcome_message'] = self._welcome_message

        super(TwitterConfiguration, self).to_yaml(data, defaults)
