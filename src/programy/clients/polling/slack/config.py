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


class SlackConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "slack")
        self._polling_interval = 1

    @property
    def polling_interval(self):
        return self._polling_interval

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, slack, bot_root, subs: Substitutions = None):
        if slack is not None:
            self._polling_interval = configuration_file.get_int_option(slack, "polling_interval", missing_value=1, subs=subs)
            super(SlackConfiguration, self).load_configuration_section(configuration_file, slack, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['polling_interval'] = 1
        else:
            data['polling_interval'] = self._polling_interval

        super(SlackConfiguration, self).to_yaml(data, defaults)