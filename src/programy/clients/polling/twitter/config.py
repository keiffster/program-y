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
from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class TwitterConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "twitter")
        self._description = 'ProgramY AIML2.0 Twitter Client'
        self._polling_interval = 0
        self._rate_limit_sleep = -1
        self._use_status = False
        self._use_direct_message = False
        self._auto_follow = False
        self._welcome_message = "Thanks for following me."

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def rate_limit_sleep(self):
        return self._rate_limit_sleep

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

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, twitter, bot_root, subs: Substitutions = None):
        if twitter is not None:
            self._polling_interval = configuration_file.get_int_option(twitter, "polling_interval", subs=subs)
            self._rate_limit_sleep = configuration_file.get_int_option(twitter, "rate_limit_sleep", missing_value=-1, subs=subs)
            self._streaming = configuration_file.get_bool_option(twitter, "streaming", subs=subs)
            self._use_status = configuration_file.get_bool_option(twitter, "use_status", subs=subs)
            self._use_direct_message = configuration_file.get_bool_option(twitter, "use_direct_message", subs=subs)
            if self._use_direct_message is True:
                self._auto_follow = configuration_file.get_bool_option(twitter, "auto_follow", subs=subs)

            self._welcome_message = configuration_file.get_option(twitter, "welcome_message", subs=subs)
            super(TwitterConfiguration, self).load_configuration_section(configuration_file, twitter, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['polling_interval'] = 0
            data['rate_limit_sleep'] = -1
            data['use_status'] = False
            data['use_direct_message'] = False
            data['auto_follow'] = False
            data['storage'] = 'file'
            data['storage_location'] = './storage/twitter.data'
            data['welcome_message'] = "Thanks for following me."
        else:
            data['polling_interval'] = self._polling_interval
            data['rate_limit_sleep'] = self._rate_limit_sleep
            data['use_status'] = self._use_status
            data['use_direct_message'] = self._use_direct_message
            data['auto_follow'] = self._auto_follow
            data['welcome_message'] = self._welcome_message

        super(TwitterConfiguration, self).to_yaml(data, defaults)