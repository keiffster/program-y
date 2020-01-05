"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
# Ignore pylint warning, this import from Programy must be before ElementTree
# Which ensures that the class LineNumberingParser is injected into the code
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order
from programy.utils.logging.ylogger import YLogger
from programy.config.file.file import BaseConfigurationFile
from programy.config.programy import ProgramyConfiguration
from programy.utils.substitutions.substitues import Substitutions


class XMLConfigurationFile(BaseConfigurationFile):

    def __init__(self):
        BaseConfigurationFile.__init__(self)
        self.xml_data = None

    def load_from_text(self, text, client_configuration, bot_root, subs: Substitutions = None):
        tree = ET.fromstring(text)
        self.xml_data = tree
        configuration = ProgramyConfiguration(client_configuration)
        configuration.load_config_data(self, bot_root, subs)
        return configuration

    def load_from_file(self, filename, client_configuration, bot_root, subs: Substitutions = None):
        configuration = ProgramyConfiguration(client_configuration)

        try:
            with open(filename, 'r+', encoding="utf-8") as xml_data_file:
                tree = ET.parse(xml_data_file, parser=LineNumberingParser())
                self.xml_data = tree.getroot()
                configuration.load_config_data(self, bot_root, subs)

        except Exception as excep:
            YLogger.exception(self, "Failed to open xml config file [%s]", excep, filename)

        return configuration

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.xml_data.find(section_name)
        return parent_section.find(section_name)

    def get_keys(self, section):
        keys = []
        for child in section:
            keys.append(child.tag)
        return keys

    def get_child_section_keys(self, child_section_name, parent_section):
        found = parent_section.find(child_section_name)
        if found is not None:
            keys = []
            for child in found:
                keys.append(child.tag)
            return keys
        return None

    def get_option(self, section, option_name, missing_value=None, subs=None):
        child = section.find(option_name)
        if child is not None:
            has_children = False
            for _ in child:
                has_children = True
                break

            if has_children is False:
                value = self._replace_subs(subs, child.text)
                return self._infer_type_from_string(value)

            return child

        if missing_value is not None:
            YLogger.warning(self, "Missing value for [%s] in config, return default value %s", option_name,
                            missing_value)

            return missing_value

    def _infer_type_from_string(self, text):
        if text == 'True' or text == 'true':
            return True
        elif text == 'False' or text == 'false':
            return False
        return text

    def get_bool_option(self, section, option_name, missing_value=False, subs: Substitutions = None):
        child = section.find(option_name)
        if child is not None:
            value = self._replace_subs(subs, child.text)
            try:
                return self.convert_to_bool(value)
            except Exception:
                pass

        YLogger.warning(self, "Missing value for [%s] in config, return default value %s", option_name,
                        missing_value)
        return missing_value

    def get_int_option(self, section, option_name, missing_value=0, subs=None):
        child = section.find(option_name)
        if child is not None:
            try:
                value = self._replace_subs(subs, child.text)
                return self.convert_to_int(value)

            except Exception as excep:
                pass

        if missing_value is not None:
            YLogger.warning(self, "Missing value for [%s] in config, return default value %d", option_name,
                            missing_value)
        else:
            YLogger.warning(self, "Missing value for [%s] in config, return default value None", option_name)

        return missing_value

    def get_multi_option(self, section, option_name, missing_value=[], subs: Substitutions = None):

        subsections = section.findall(option_name)

        values = []
        for child in subsections:
            if child.text:
                text = child.text
                text = text.strip()
                values.append(self._replace_subs(subs, text))

        if values:
            return values

        return missing_value

    def get_multi_file_option(self, section, option_name, bot_root, missing_value=[], subs: Substitutions = None):

        value = self.get_option(section, option_name, missing_value, subs)

        if isinstance(value, list):
            if value:
                return self._replace_subs(subs, value)

        if isinstance(value, str):
            values = [self._replace_subs(subs, value)]

        else:
            values = []
            if len(value):
                for child in value:
                    if child.tag == "dir":
                        replaced = self._replace_subs(subs, child.text)
                        if replaced:
                            values.append(replaced)

        multis = []
        for value in values:
            multis.append(value.replace('$BOT_ROOT', bot_root))

        return multis
