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

from programy.config.base import BaseConfigurationData

class RestConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "rest")
        self._host = "0.0.0.0"
        self._port = 80
        self._debug = False
        self._workers = 4
        self._use_api_keys = False
        self._api_key_file = None

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
    def workers(self):
        return self._workers

    @property
    def use_api_keys(self):
        return self._use_api_keys

    @property
    def api_key_file(self):
        return self._api_key_file

    def load_config_section(self, config_file, bot_root):
        rest = config_file.get_section(self.section_name)
        if rest is not None:
            self._host = config_file.get_option(rest, "host", missing_value="0.0.0.0")
            self._port = config_file.get_option(rest, "port", missing_value=80)
            self._debug = config_file.get_bool_option(rest, "debug", missing_value=False)
            self._workers = config_file.get_option(rest, "workers", missing_value=4)
            self._use_api_keys = config_file.get_bool_option(rest, "use_api_keys", missing_value=False)
            self._api_key_file = config_file.get_option(rest, "api_key_file")
            if self._api_key_file is not None:
                self._api_key_file = self.sub_bot_root(self._api_key_file, bot_root)
