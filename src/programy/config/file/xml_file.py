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

from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

import logging
from programy.config.file.file import BaseConfigurationFile

class XMLConfigurationFile(BaseConfigurationFile):

    def __init__(self, client_config):
        BaseConfigurationFile.__init__(self, client_config)
        self.xml_data = None

    def load_from_text(self, text, bot_root):
        tree = ET.fromstring(text)
        self.xml_data = tree
        self.client_config.load_config_data(self, bot_root)

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as xml_data_file:
            tree = ET.parse(xml_data_file, parser=LineNumberingParser())
            self.xml_data = tree.getroot()
            self.client_config.load_config_data(self, bot_root)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.xml_data.find(section_name)
        else:
            return parent_section.find(section_name)

    def get_section_data(self, section_name, parent_section=None):
        if parent_section is None:
            section = self.xml_data.find(section_name)
        else:
            section = parent_section.find(section_name)
        data = {}
        for child in section:
            data[child.tag] = child.text
        return data

    def get_child_section_keys(self, section_name, parent_section=None):
        keys = []
        if parent_section is None:
            for child in self.xml_data.find(section_name):
                keys.append(child.tag)
        else:
            for child in parent_section.find(section_name):
                keys.append(child.tag)
        return keys

    def get_option(self, section, option_name, missing_value=None):
        child = section.find(option_name)
        if child is not None:
            return self._infer_type_from_string(child.text)
        else:
            if missing_value is not None:
                logging.warning("Missing value for [%s] in config, return default value %s", option_name, missing_value)
            return missing_value

