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

import logging
from programy.config.base import BaseConfigurationData

class BrainFileConfiguration(object):

    def __init__(self, file=None, files=None, extension=".aiml", directories=False, errors=None, duplicates=None):
        self._file = None
        self._files = None
        self._extension = None
        self._directories = None
        self._errors = None
        self._duplicates = None

        if file is not None:
            self._file = file
        else:
            self._files = files
            self._extension = extension
            self._directories = directories

        self._errors = errors
        self._duplicates = duplicates

    @property
    def file(self):
        return self._file

    def is_single_file(self):
        return bool(self._file is not None)

    @property
    def files(self):
        return self._files

    @property
    def extension(self):
        return self._extension

    @property
    def directories(self):
        return self._directories

    @property
    def errors(self):
        return self._errors

    @property
    def duplicates(self):
        return self._duplicates


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
        self._params[key.upper()] = value

    def parameter(self, name):
        if name in self._params:
            return self._params[name]
        else:
            return None


class BrainConfiguration(BaseConfigurationData):

    DEFAULT_SUPRESS_WARNINGS    = False
    DEFAULT_ALLOW_SYSTEM_AIML   = True
    DEFAULT_ALLOW_LEARN_AIML    = True
    DEFAULT_ALLOW_LEARNF_AIML   = True

    def __init__(self):
        self._allow_system_aiml = BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML
        self._allow_learn_aiml  = BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML
        self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML
        self._pattern_nodes     = None
        self._template_nodes    = None
        self._dump_to_file      = None
        self._aiml_files        = None
        self._set_files         = None
        self._map_files         = None
        self._denormal          = None
        self._normal            = None
        self._gender            = None
        self._person            = None
        self._person2           = None
        self._predicates        = None
        self._pronouns          = None
        self._properties        = None
        self._triples           = None
        self._preprocessors     = None
        self._postprocessors    = None
        self._services = []
        BaseConfigurationData.__init__(self, "brain")

    def _get_brain_file_configuration(self, config_file, section, bot_root):
        errors = config_file.get_option(section, "errors", missing_value=None)
        duplicates = config_file.get_option(section, "duplicates", missing_value=None)

        files = config_file.get_option(section, "files")
        if files is not None:
            files = self.sub_bot_root(files, bot_root)
            extension = config_file.get_option(section, "extension")
            directories = config_file.get_option(section, "directories")
            return BrainFileConfiguration(files=files, extension=extension, directories=directories, errors=errors, duplicates=duplicates)
        else:
            file = config_file.get_option(section, "file")
            file = self.sub_bot_root(file, bot_root)
            return BrainFileConfiguration(file=file, errors=errors, duplicates=duplicates)

    def load_config_section(self, config_file, bot_root):

        brain = config_file.get_section(self.section_name)
        if brain is not None:
            self._allow_system_aiml = config_file.get_option(brain, "allow_system_aiml", BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML)
            self._allow_learn_aiml = config_file.get_option(brain, "allow_learn_aiml", BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML)
            self._allow_learnf_aiml = config_file.get_option(brain, "allow_learnf_aiml", BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML)
            self._allow_learnf_aiml = config_file.get_option(brain, "allow_learnf_aiml", BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML)
            self._pattern_nodes = config_file.get_option(brain, "pattern_nodes", missing_value=None)
            self._template_nodes = config_file.get_option(brain, "template_nodes", missing_value=None)
            self._dump_to_file = config_file.get_option(brain, "dump_to_file", missing_value=None)

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
                logging.warning("Config section [files] missing from Brain, default values not appropriate")
                raise Exception ("Config section [files] missing from Brain")

            services = config_file.get_section("services", brain)
            if services is not None:
                service_keys = config_file.get_child_section_keys("services", brain)

                for name in service_keys:
                    service_data = config_file.get_section_data(name, services)
                    self._services.append(BrainServiceConfiguration(name, service_data))

            else:
                logging.warning("Config section [services] missing from Brain, no services loaded")
        else:
            logging.warning("Config section [%s] missing, using default values", self.section_name)
            self._allow_system_aiml = BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML
            self._allow_learn_aiml  = BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML
            self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML
            self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML
            self._pattern_nodes     = None
            self._template_nodes    = None
            self._dump_to_file      = None

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
    def pattern_nodes(self):
        return self._pattern_nodes

    @property
    def template_nodes(self):
        return self._template_nodes

    @property
    def dump_to_file(self):
        return self._dump_to_file

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


