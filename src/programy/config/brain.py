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

    DEFAULT_SUPRESS_WARNINGS    = False
    DEFAULT_ALLOW_SYSTEM_AIML   = True
    DEFAULT_ALLOW_LEARN_AIML    = True
    DEFAULT_ALLOW_LEARNF_AIML   = True

    def __init__(self):
        self._supress_warnings  = BrainConfiguration.DEFAULT_SUPRESS_WARNINGS
        self._allow_system_aiml = BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML
        self._allow_learn_aiml  = BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML
        self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML
        self._aiml_files        = None
        self._set_files         = None
        self._map_files         = None
        self._license_keys      = None
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
            self._supress_warnings = config_file.get_option("supress_warnings", brain, BrainConfiguration.DEFAULT_SUPRESS_WARNINGS)
            self._allow_system_aiml = config_file.get_option("allow_system_aiml", brain, BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML)
            self._allow_learn_aiml = config_file.get_option("allow_learn_aiml", brain, BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML)
            self._allow_learnf_aiml = config_file.get_option("allow_learnf_aiml", brain, BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML)
            self._allow_learnf_aiml = config_file.get_option("allow_learnf_aiml", brain, BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML)

            files = config_file.get_section("files", brain)
            if files is not None:
                aiml = config_file.get_section("aiml", files)
                self._aiml_files = self._get_brain_file_configuration(config_file, aiml, bot_root)

                sets = config_file.get_section("sets", files)
                self._set_files = self._get_brain_file_configuration(config_file, sets, bot_root)

                maps = config_file.get_section("maps", files)
                self._map_files = self._get_brain_file_configuration(config_file, maps, bot_root)

                self._license_keys = self._get_file_option(config_file, "license_keys", files, bot_root)
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
            self._supress_warnings  = BrainConfiguration.DEFAULT_SUPRESS_WARNINGS
            self._allow_system_aiml = BrainConfiguration.DEFAULT_ALLOW_SYSTEM_AIML
            self._allow_learn_aiml  = BrainConfiguration.DEFAULT_ALLOW_LEARN_AIML
            self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML
            self._allow_learnf_aiml = BrainConfiguration.DEFAULT_ALLOW_LEARNF_AIML

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
    def license_keys(self):
        return self._license_keys

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


