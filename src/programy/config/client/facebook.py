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

class FacebookConfiguration(BaseConfigurationData):

    def __init__(self):
        self._polling = False
        self._polling_interval = 0
        self._streaming = False
        BaseConfigurationData.__init__(self, "facebook")

    @property
    def polling(self):
        return self._polling

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def streaming(self):
        return self._streaming

    def load_config_section(self, config_file, bot_root):
        facebook = config_file.get_section(self.section_name)
        if facebook is not None:
            self._polling = config_file.get_bool_option(facebook, "polling")
            if self._polling is True:
                self._polling_interval = config_file.get_int_option(facebook, "polling_interval")
            self._streaming = config_file.get_bool_option(facebook, "streaming")

class FacebookClientConfiguration(ClientConfiguration):

    def __init__(self):
        ClientConfiguration.__init__(self)
        self._facebook_config = FacebookConfiguration()

    @property
    def facebook_configuration(self):
        return self._facebook_config

    def load_config_data(self, config_file, bot_root):
        super(FacebookClientConfiguration, self).load_config_data(config_file, bot_root)
        self._facebook_config.load_config_section(config_file, bot_root)
