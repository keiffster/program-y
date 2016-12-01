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

    def __init__(self, files, extension, directories):
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


class BrainConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "brain")
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

    def get_file_option(self, config_file, option_name, section, bot_root):
        option = config_file.get_option(option_name, section)
        if option is not None:
            option = self.sub_bot_root(option, bot_root)
        return option

    def load_config_section(self, config_file, bot_root):

        brain = config_file.get_section(self.section_name)

        self._supress_warnings = config_file.get_option("supress_warnings", brain)
        self._allow_system_aiml = config_file.get_option("allow_system_aiml", brain)
        self._allow_learn_aiml = config_file.get_option("allow_learn_aiml", brain)
        self._allow_learnf_aiml = config_file.get_option("allow_learnf_aiml", brain)

        files = config_file.get_section("files", brain)

        aiml = config_file.get_section("aiml", files)
        self._aiml_files = self.get_brain_file_configuration(config_file, aiml, bot_root)

        sets = config_file.get_section("sets", files)
        self._set_files = self.get_brain_file_configuration(config_file, sets, bot_root)

        maps = config_file.get_section("maps", files)
        self._map_files = self.get_brain_file_configuration(config_file, maps, bot_root)

        self._denormal          = self.get_file_option(config_file, "denormal", files, bot_root)
        self._normal            = self.get_file_option(config_file, "normal", files, bot_root)
        self._gender            = self.get_file_option(config_file, "gender", files, bot_root)
        self._person            = self.get_file_option(config_file, "person", files, bot_root)
        self._person2           = self.get_file_option(config_file, "person2", files, bot_root)
        self._predicates        = self.get_file_option(config_file, "predicates", files, bot_root)
        self._pronouns          = self.get_file_option(config_file, "pronouns", files, bot_root)
        self._properties        = self.get_file_option(config_file, "properties", files, bot_root)
        self._triples           = self.get_file_option(config_file, "triples", files, bot_root)
        self._preprocessors     = self.get_file_option(config_file, "preprocessors", files, bot_root)
        self._postprocessors    = self.get_file_option(config_file, "postprocessors", files, bot_root)

    def get_brain_file_configuration(self, config_file, section, bot_root):
        files = config_file.get_option("files", section)
        files = self.sub_bot_root(files, bot_root)
        extension = config_file.get_option("extension", section)
        directories = config_file.get_option("directories", section)
        return BrainFileConfiguration(files, extension, directories)

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

        self._prompt = config_file.get_option("prompt", bot)
        self._default_response = config_file.get_option("default_response", bot)
        self._exit_response = config_file.get_option("exit_response", bot)
        self._initial_question = config_file.get_option("initial_question", bot)

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


class BaseConfigurationFile(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.client_config = self.get_client_configuration()

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        return ClientConfiguration()

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
    def get_option(self, section, option_name):
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

    def __init__(self):
        BaseConfigurationFile.__init__(self)

    def load_from_text(self, text, bot_root):
        self.yaml_data = yaml.load(text)
        self.client_config.load_config_data(self)

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as yml_data_file:
            self.yaml_data = yaml.load(yml_data_file)
            self.client_config.load_config_data(self, bot_root)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.yaml_data[section_name]
        else:
            return parent_section[section_name]

    def get_option(self, option_name, section):
        return section[option_name]


class JSONConfigurationFile(BaseConfigurationFile):

    def __init__(self):
        BaseConfigurationFile.__init__(self)

    def load_from_text(self, text, bot_root):
        #TODO To implement
        raise Exception("Not implemented yet")

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as json_data_file:
            self.json_data = json.load(json_data_file)
            self.client_config.load_config_data(self)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.json_data[section_name]
        else:
            return parent_section[section_name]

    def get_option(self, option_name, section):
        return section[option_name]


class XMLConfigurationFile(BaseConfigurationFile):

    def __init__(self):
        BaseConfigurationFile.__init__(self)

    def load_from_text(self, text, bot_root):
        # TODO To implement
        raise Exception("Not implemented yet")

    def load_from_file(self, filename, bot_root):
        with open(filename, 'r+') as xml_data_file:
            tree = ET.parse(xml_data_file, parser=LineNumberingParser())
            self.xml_data = tree.getroot()
            self.client_config.load_config_data(self)

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            return self.xml_data.find(section_name)
        else:
            return parent_section.find(section_name)

    def get_option(self, option_name, section):
        child = section.find(option_name)
        return self._infer_type_from_string(child.text)


class ConfigurationFactory(object):

    @classmethod
    def load_configuration_from_file(cls, filename, format=None, bot_root="."):

        if format is None or len(format) == 0:
            format = ConfigurationFactory.guess_format_from_filename(filename)

        config_file = ConfigurationFactory.get_config_by_name(format)
        config_file.load_from_file(filename, bot_root)
        return config_file.client_config

    @classmethod
    def guess_format_from_filename(cls, filename):
        if "." not in filename:
            raise Exception ("No file extension to allow format guessing!")

        last_dot = filename.rfind(".")
        format = filename[last_dot + 1:]
        return format

    @classmethod
    def get_config_by_name(cls, format):
        format = format.lower()

        if format == 'yaml':
            return YamlConfigurationFile()
        elif format == 'json':
            return JSONConfigurationFile()
        elif format == 'xml':
            return XMLConfigurationFile()
        else:
            raise Exception("Unsupported configuration format:", format)
