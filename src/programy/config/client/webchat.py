"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without webchatriction, including without limitation
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

class WebChatConfiguration(BaseConfigurationData):

    def __init__(self):
        self._host = "0.0.0.0"
        self._port = 80
        self._debug = False
        self._use_api_keys = False
        BaseConfigurationData.__init__(self, "webchat")

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def debug(self):
        return self._debug

    @property
    def use_api_keys(self):
        return self._use_api_keys

    def load_config_section(self, config_file, bot_root):
        webchat = config_file.get_section(self.section_name)
        if webchat is not None:
            self._host = config_file.get_option(webchat, "host")
            self._port = config_file.get_option(webchat, "port")
            self._debug = config_file.get_bool_option(webchat, "debug")
            self._use_api_keys = config_file.get_bool_option(webchat, "use_api_keys")

class WebChatClientConfiguration(ClientConfiguration):

    def __init__(self):
        ClientConfiguration.__init__(self)
        self._webchat_config = WebChatConfiguration()

    @property
    def webchat_configuration(self):
        return self._webchat_config

    def load_config_data(self, config_file, bot_root):
        super(WebChatClientConfiguration, self).load_config_data(config_file, bot_root)
        self._webchat_config.load_config_section(config_file, bot_root)
