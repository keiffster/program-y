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


class TelegramConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "telegram")
        self._unknown_command = None
        self._unknown_command_srai = None

    @property
    def unknown_command(self):
        return self._unknown_command

    @property
    def unknown_command_srai(self):
        return self._unknown_command_srai

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, telegram, bot_root, subs: Substitutions = None):
        if telegram is not None:
            self._unknown_command = configuration_file.get_option(telegram, "unknown_command", missing_value="Unknown command", subs=subs)
            self._unknown_command_srai = configuration_file.get_option(telegram, "unknown_command_srai", missing_value=None, subs=subs)
            super(TelegramConfiguration, self).load_configuration_section(configuration_file, telegram, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['unknown_command'] = "Sorry, that is not a command I have been taught yet!"
            data['unknown_command_srai'] = 'YTELEGRAM_UNKNOWN_COMMAND'
        else:
            data['unknown_command'] = self._unknown_command
            data['unknown_command_srai'] = self._unknown_command_srai

        super(TelegramConfiguration, self).to_yaml(data, defaults)