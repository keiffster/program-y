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

import yaml
import json
import logging
from abc import ABCMeta, abstractmethod


class BaseConfigurationData(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.section_name = name

    def sub_bot_root(self, text, root):
        return text.replace('$BOT_ROOT', root)

    @abstractmethod
    def load_config_section(self, config_file, bot_root):
        """
        Never Implemented
        """

class BrainFileConfiguration(object):

    def __init__(self, files, extension=".aiml", directories=False):
        self._files = files
        self._extension = extension
        self._directories = directories

    @property
    def files(self):
        return self._files

    @property
    def extension(self):
        return self._extension

    @property
    def directories(self):
        return self._directories


class BrainServiceConfiguration(object):

    def __init__(self, name, data=None):
        self._name = name.upper()
        self._params = {}
        if data is not None:
            for key in data.keys():
                self._params[key.upper()] = data[key]

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._params['PATH']

    def parameters(self):
        return self._params.keys()

    def set_parameter(self, key, value):
        self._params[key] = value

    def parameter(self, name):
        if name in self._params:
            return self._params[name]
        else:
            return None


class BrainConfiguration(BaseConfigurationData):

    def __init__(self):
        self._supress_warnings = False
        self._allow_system_aiml = True
        self._allow_learn_aiml = True
        self._allow_learnf_aiml = True
        self._aiml_files = None
        self._set_files = None
        self._map_files = None
        self._denormal = None
        self._normal = None
        self._gender = None
        self._person = None
        self._person2 = None
        self._predicates = None
        self._pronouns = None
        self._properties = None
        self._triples = None
        self._preprocessors = None
        self._postprocessors = None
        self._services = []
        BaseConfigurationData.__init__(self, "brain")

    def _get_file_option(self, config_file, option_name, section, bot_root):
        option = config_file.get_option(option_name, section)
        if option is not None:
            option = self.sub_bot_root(option, bot_root)
        return option

    def _get_brain_file_configuration(self, config_file, section, bot_root):
        files = config_file.get_option("files", section)
        files = self.sub_bot_root(files, bot_root)
        extension = config_file.get_option("extension", section)
        directories = config_file.get_option("directories", section)
        return BrainFileConfiguration(files, extension, directories)

    def load_config_section(self, config_file, bot_root):

        brain = config_file.get_section(self.section_name)
        if brain is not None:
            self._supress_warnings = config_file.get_option("supress_warnings", brain)
            self._allow_system_aiml = config_file.get_option("allow_system_aiml", brain)
            self._allow_learn_aiml = config_file.get_option("allow_learn_aiml", brain)
            self._allow_learnf_aiml = config_file.get_option("allow_learnf_aiml", brain)

            files = config_file.get_section("files", brain)
            if files is not None:
                aiml = config_file.get_section("aiml", files)

                self._aiml_files = self._get_brain_file_configuration(config_file, aiml, bot_root)

                sets = config_file.get_section("sets", files)
                self._set_files = self._get_brain_file_configuration(config_file, sets, bot_root)

                maps = config_file.get_section("maps", files)
                self._map_files = self._get_brain_file_configuration(config_file, maps, bot_root)

                self._denormal = self._get_file_option(config_file, "denormal", files, bot_root)
                self._normal = self._get_file_option(config_file, "normal", files, bot_root)
                self._gender = self._get_file_option(config_file, "gender", files, bot_root)
                self._person = self._get_file_option(config_file, "person", files, bot_root)
                self._person2 = self._get_file_option(config_file, "person2", files, bot_root)
                self._predicates = self._get_file_option(config_file, "predicates", files, bot_root)
                self._pronouns = self._get_file_option(config_file, "pronouns", files, bot_root)
                self._properties = self._get_file_option(config_file, "properties", files, bot_root)
                self._triples = self._get_file_option(config_file, "triples", files, bot_root)
                self._preprocessors = self._get_file_option(config_file, "preprocessors", files, bot_root)
                self._postprocessors = self._get_file_option(config_file, "postprocessors", files, bot_root)
            else:
                logging.warning("Config section [files] missing from Brain")

            services = config_file.get_section("services", brain)
            if services is not None:
                service_keys = config_file.get_child_section_keys("services", brain)

                for name in service_keys:
                    service_data = config_file.get_section_data(name, services)
                    self._services.append(BrainServiceConfiguration(name, service_data))

            else:
                logging.warning("Config section [services] missing from Brain")
        else:
            logging.warning("Config section [%s] missing", self.section_name)

    @property
    def supress_warnings(self):
        return self._supress_warnings

    @property
    def allow_system_aiml(self):
        return self._allow_system_aiml

    @property
    def allow_learn_aiml(self):
        return self._allow_learn_aiml

    @property
    def allow_learnf_aiml(self):
        return self._allow_learnf_aiml

    @property
    def aiml_files(self):
        return self._aiml_files

    @property
    def set_files(self):
        return self._set_files

    @property
    def map_files(self):
        return self._map_files

    @property
    def denormal(self):
        return self._denormal

    @property
    def normal(self):
        return self._normal

    @property
    def gender(self):
        return self._gender

    @property
    def person(self):
        return self._person

    @property
    def person2(self):
        return self._person2

    @property
    def predicates(self):
        return self._predicates

    @property
    def pronouns(self):
        return self._pronouns

    @property
    def properties(self):
        return self._properties

    @property
    def triples(self):
        return self._triples

    @property
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    @property
    def services(self):
        return self._services


class BotConfiguration(BaseConfigurationData):

    def __init__(self):
        self.bot_root = "."
        self._prompt = ">>> "
        self._default_response = "Sorry, I don't have an answer for that right now"
        self._exit_response = "Bye!"
        self._initial_question = "Hello"
        BaseConfigurationData.__init__(self, "bot")

    def load_config_section(self, config_file, bot_root):
        bot = config_file.get_section(self.section_name)
        if bot is not None:
            self._prompt = config_file.get_option("prompt", bot)
            self._default_response = config_file.get_option("default_response", bot)
            self._exit_response = config_file.get_option("exit_response", bot)
            self._initial_question = config_file.get_option("initial_question", bot)
        else:
            logging.warning("Config section [%s] missing", self.section_name)

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, text):
        self._prompt = text

    @property
    def default_response(self):
        return self._default_response

    @default_response.setter
    def default_response(self, text):
        self._default_response = text

    @property
    def exit_response(self):
        return self._exit_response

    @exit_response.setter
    def exit_response(self, text):
        self._exit_response = text

    @property
    def initial_question(self):
        return self._initial_question

    @initial_question.setter
    def initial_question(self, text):
        self._initial_question = text


class RestConfiguration(BaseConfigurationData):

    def __init__(self):
        self._host = "0.0.0.0"
        self._port = 80
        self._debug = False
        self._use_api_keys = False
        BaseConfigurationData.__init__(self, "rest")

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
        rest = config_file.get_section(self.section_name)
        if rest is not None:
            self._host = config_file.get_option("host", rest)
            self._port = config_file.get_option("port", rest)
            self._debug = config_file.get_bool_option("debug", rest)
            self._use_api_keys = config_file.get_bool_option("use_api_keys", rest)


class ClientConfiguration(object):

    def __init__(self):
        self._brain_config = BrainConfiguration()
        self._bot_config = BotConfiguration()

    @property
    def brain_configuration(self):
        return self._brain_config

    @property
    def bot_configuration(self):
        return self._bot_config

    def load_config_data(self, config_file, bot_root):
        self._brain_config.load_config_section(config_file, bot_root)
        self._bot_config.load_config_section(config_file, bot_root)


class RestClientConfiguration(ClientConfiguration):

    def __init__(self):
        ClientConfiguration.__init__(self)
        self._rest_config = RestConfiguration()

    @property
    def rest_configuration(self):
        return self._rest_config

    def load_config_data(self, config_file, bot_root):
        super(RestClientConfiguration, self).load_config_data(config_file, bot_root)
        self._rest_config.load_config_section(config_file, bot_root)


class BaseConfigurationFile(object):
    __metaclass__ = ABCMeta

    def __init__(self, client_config):
        self.client_config = client_config

    @abstractmethod
    def load_from_text(self, text, bot_root):
        """
        Never Implemented
        """

    @abstractmethod
    def load_from_file(self, filename, bot_root):
        """
        Never Implemented
        """

    @abstractmethod
    def get_section(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    def get_section_data(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    def get_child_section_keys(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    #TODO option_name and section are the wrong way round to other function calls
    def get_option(self, option_name, section, missing_value=None):
        """
        Never Implemented
        """

    def _infer_type_from_string(self, text):
        if text == 'True' or text == 'true':
            return True
        elif text == 'False' or text == 'false':
            return False
        else:
            return text


class YamlConfigurationFile(BaseConfigurationFile):

    def __init__(self, client_config):
        BaseConfigurationFile.__init__(self, client_config)
        self.yaml_data = None

    def load_from_text(self, text, bot_root):
        self.yaml_data = yaml.load(text)
        self.client_config.load_config_data(self, bot_root)

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as yml_data_file:
            self.yaml_data = yaml.load(yml_data_file)
            self.client_config.load_config_data(self, bot_root)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            if section_name in self.yaml_data:
                return self.yaml_data[section_name]
        else:
            if section_name in parent_section:
                return parent_section[section_name]
        return None

    def get_section_data(self, section_name, parent_section=None):
        return self.get_section(section_name, parent_section)

    def get_child_section_keys(self, section_name, parent_section=None):
        if parent_section is None:
            return self.yaml_data[section_name].keys()
        else:
            return parent_section[section_name].keys()

    def get_option(self, option_name, section, missing_value=None):
        if option_name in section:
            return section[option_name]
        else:
            logging.error("Missing value for [%s] in config section [%s], return default value %s", option_name, section, missing_value)
            return missing_value

    def get_bool_option(self, option_name, section, missing_value=False):
        if option_name in section:
            value = section[option_name]
            if isinstance(value, bool):
                return bool(value)
            else:
                raise Exception("Invalid boolean config value")
        else:
            logging.error("Missing value for [%s] in config section [%s], return default value %s", option_name, section, missing_value)
            return missing_value

    def get_int_option(self, option_name, section, missing_value=0):
        if option_name in section:
            value = section[option_name]
            if isinstance(value, int):
                return int(value)
            else:
                raise Exception("Invalid integer config value")
        else:
            logging.error("Missing value for [%s] in config section [%s], return default value %d", option_name, section, missing_value)
            return missing_value


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

    def get_option(self, option_name, section, missing_value=None):
        if option_name in section:
            return section[option_name]
        else:
            logging.error("Missing value for [%s] in config section [%s], return default value %s", option_name, section, missing_value)
            return missing_value


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

    def get_option(self, option_name, section, missing_value=None):
        child = section.find(option_name)
        if child is not None:
            return self._infer_type_from_string(child.text)
        else:
            logging.error("Missing value for [%s] in config section [%s], return default value %s", option_name, section, missing_value)
            return missing_value


class ConfigurationFactory(object):

    @classmethod
    def load_configuration_from_file(cls, client_config, filename, file_format=None, bot_root="."):

        if file_format is None or len(file_format) == 0:
            file_format = ConfigurationFactory.guess_format_from_filename(filename)

        config_file = ConfigurationFactory.get_config_by_name(client_config, file_format)
        config_file.load_from_file(filename, bot_root)
        return config_file

    @classmethod
    def guess_format_from_filename(cls, filename):
        if "." not in filename:
            raise Exception("No file extension to allow format guessing!")

        last_dot = filename.rfind(".")
        file_format = filename[last_dot + 1:]
        return file_format

    @classmethod
    def get_config_by_name(cls, client_config, file_format):
        file_format = file_format.lower()

        if file_format == 'yaml':
            return YamlConfigurationFile(client_config)
        elif file_format == 'json':
            return JSONConfigurationFile(client_config)
        elif file_format == 'xml':
            return XMLConfigurationFile(client_config)
        else:
            raise Exception("Unsupported configuration format:", file_format)
