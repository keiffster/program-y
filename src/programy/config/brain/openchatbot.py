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
from programy.utils.logging.ylogger import YLogger

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainOpenChatBotConfiguration(BaseSectionConfigurationData):

    def __init__(self, openchatbot_name):
        BaseSectionConfigurationData.__init__(self, openchatbot_name)
        self._url = None
        self._method = None
        self._authorization = None
        self._api_key = None

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @property
    def authorization(self):
        return self._authorization

    @property
    def api_key(self):
        return self._api_key

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        openchatbot = configuration_file.get_section(self.section_name, configuration)
        if openchatbot is not None:
            self._url = configuration_file.get_option(openchatbot, "url", missing_value=None, subs=subs)
            self._method = configuration_file.get_option(openchatbot, "method", missing_value="GET", subs=subs)
            self._authorization = configuration_file.get_option(openchatbot, "authorization", subs=subs)
            self._api_key = configuration_file.get_option(openchatbot, "api_key", subs=subs)
            self.load_additional_key_values(configuration_file, openchatbot)
        else:
            YLogger.warning(self, "'openchatbot' section missing from brain config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['url'] = self._url
            data['method'] = self._method
            data['authorization'] = self._authorization
            data['api_key'] = self._api_key
        else:
            data['url'] = None
            data['method'] = None
            data['authorization'] = None
            data['api_key'] = None
