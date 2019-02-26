"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial avatarions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.clients.restful.config import RestConfiguration
from programy.utils.substitutions.substitues import Substitutions


class LineConfiguration(RestConfiguration):

    def __init__(self):
        RestConfiguration.__init__(self, "line")
        self._unknown_command = "Unknown command"
        self._unknown_command_srai = None

    @property
    def unknown_command(self):
        return self._unknown_command

    @property
    def unknown_command_srai(self):
        return self._unknown_command_srai

    def check_for_license_keys(self, license_keys):
        RestConfiguration.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, line, bot_root, subs: Substitutions = None):
        if line is not None:
            self._unknown_command = configuration_file.get_option(line, "unknown_command", missing_value="Unknown command", subs=subs)
            self._unknown_command_srai = configuration_file.get_option(line, "unknown_command_srai", missing_value=None, subs=subs)
            super(LineConfiguration, self).load_configuration_section(configuration_file, line, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['unknown_command'] = "Unknown command"
            data['unknown_command_srai'] = 'LINEUNKNOWNCOMMAND'
        else:
            data['unknown_command'] = self._unknown_command
            data['unknown_command_srai'] = self._unknown_command_srai

        super(LineConfiguration, self).to_yaml(data, defaults)