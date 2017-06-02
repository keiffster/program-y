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

import json

import logging
from programy.config.file.file import BaseConfigurationFile


class JSONConfigurationFile(BaseConfigurationFile):

    def __init__(self, client_config):
        BaseConfigurationFile.__init__(self, client_config)
        self.json_data = None

    def load_from_text(self, text, bot_root):
        self.json_data = json.loads(text)
        self.client_config.load_config_data(self, bot_root)

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as json_data_file:
            self.json_data = json.load(json_data_file)
            self.client_config.load_config_data(self, bot_root)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.json_data[section_name]
        else:
            return parent_section[section_name]

    def get_section_data(self, section_name, parent_section=None):
        return self.get_section(section_name, parent_section)

    def get_child_section_keys(self, section_name, parent_section=None):
        if parent_section is None:
            return self.json_data[section_name].keys()
        else:
            return parent_section[section_name].keys()

    def get_option(self, section, option_name, missing_value=None):
        if option_name in section:
            return section[option_name]
        else:
            logging.warning("Missing value for [%s] in config , return default value %s", option_name, missing_value)
            return missing_value


