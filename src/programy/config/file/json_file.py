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

import json

from programy.utils.logging.ylogger import YLogger
from programy.config.file.file import BaseConfigurationFile
from programy.config.programy import ProgramyConfiguration
from programy.utils.substitutions.substitues import Substitutions


class JSONConfigurationFile(BaseConfigurationFile):

    def __init__(self):
        BaseConfigurationFile.__init__(self)
        self.json_data = None

    def load_from_text(self, text, client_configuration, bot_root):
        self.json_data = json.loads(text)
        configuration = ProgramyConfiguration(client_configuration)
        configuration.load_config_data(self, bot_root)
        return configuration

    def load_from_file(self, filename, client_configuration, bot_root):
        configuration = ProgramyConfiguration(client_configuration)
        try:
            with open(filename, 'r+', encoding="utf-8") as json_data_file:
                self.json_data = json.load(json_data_file)
                configuration.load_config_data(self, bot_root)

        except Exception as excep:
            YLogger.exception(self, "Failed to open json config file [%s]", excep, filename)

        return configuration

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            if section_name in self.json_data:
                return self.json_data[section_name]
        else:
            if section_name in parent_section:
                return parent_section[section_name]
        return None

    def get_keys(self, section):
        return section.keys()

    def get_child_section_keys(self, child_section_name, parent_section):
        if child_section_name in parent_section:
            return parent_section[child_section_name].keys()
        return None

    def get_option(self, section, option_name, missing_value=None, subs: Substitutions = None):
        if option_name in section:
            option_value = section[option_name]
            return self._replace_subs(subs, option_value)

        YLogger.warning(self, "Missing value for [%s] in config , return default value %s", option_name, missing_value)
        return missing_value

    def get_bool_option(self, section, option_name, missing_value=False, subs: Substitutions = None):
        if option_name in section:
            option_value = section[option_name]
            if isinstance(option_value, bool):
                return option_value
            return bool(self._replace_subs(subs, option_value))

        YLogger.warning(self, "Missing value for [%s] in config, return default value %s", option_name, missing_value)
        return missing_value

    def get_int_option(self, section, option_name, missing_value=0, subs: Substitutions = None):
        if option_name in section:
            option_value = section[option_name]
            if isinstance(option_value, int):
                return option_value
            return int(self._replace_subs(subs, option_value))

        if missing_value is not None:
            YLogger.warning(self, "Missing value for [%s] in config, return default value %d", option_name, missing_value)
        else:
            YLogger.warning(self, "Missing value for [%s] in config, return default value None", option_name)

        return missing_value

    def get_multi_option(self, section, option_name, missing_value=None, subs: Substitutions = None):
        if missing_value is None:
            missing_value = []

        value = self. get_option(section, option_name, missing_value)
        if isinstance(value, list):
            values = value

        else:
            values = [value]

        multis = []
        for value in values:
            multis.append(self._replace_subs(subs, value))

        return multis

    def get_multi_file_option(self, section, option_name, bot_root, missing_value=None, subs: Substitutions = None):
        if missing_value is None:
            missing_value = []

        value = self. get_option(section, option_name, missing_value)
        if isinstance(value, list):
            values = value

        else:
            values = [value]

        multis = []
        for value in values:
            value = self._replace_subs(subs, value)
            multis.append(value.replace('$BOT_ROOT', bot_root))

        return multis
