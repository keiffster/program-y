"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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
from programy.config.sections.brain.aiml_file import BrainAIMLFileConfiguration
from programy.config.sections.brain.file import BrainFileConfiguration

class BrainFilesConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "files")
        self._aiml_files        = BrainAIMLFileConfiguration()
        self._set_files         = BrainFileConfiguration("sets")
        self._map_files         = BrainFileConfiguration("maps")
        self._rdf_files         = BrainFileConfiguration("rdf")

        self._denormal          = None
        self._normal            = None
        self._gender            = None
        self._person            = None
        self._person2           = None
        self._properties        = None
        self._triples           = None
        self._preprocessors     = None
        self._postprocessors    = None

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
    def properties(self):
        return self._properties

    @property
    def rdf_files(self):
        return self._rdf_files

    @property
    def triples(self):
        return self._triples

    @property
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    def load_config_section(self, config_file, brain_config, bot_root):
        files_config = config_file.get_section("files", brain_config)
        if files_config is not None:
            self._aiml_files.load_config_section(config_file, files_config, bot_root)
            self._set_files.load_config_section(config_file, files_config, bot_root)
            self._map_files.load_config_section(config_file, files_config, bot_root)
            self._rdf_files.load_config_section(config_file, files_config, bot_root)

            self._denormal = self._get_file_option(config_file, "denormal", files_config, bot_root)
            self._normal = self._get_file_option(config_file, "normal", files_config, bot_root)
            self._gender = self._get_file_option(config_file, "gender", files_config, bot_root)
            self._person = self._get_file_option(config_file, "person", files_config, bot_root)
            self._person2 = self._get_file_option(config_file, "person2", files_config, bot_root)
            self._properties = self._get_file_option(config_file, "properties", files_config, bot_root)
            self._triples = self._get_file_option(config_file, "triples", files_config, bot_root)
            self._preprocessors = self._get_file_option(config_file, "preprocessors", files_config, bot_root)
            self._postprocessors = self._get_file_option(config_file, "postprocessors", files_config, bot_root)
        else:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Config section [files] missing from Brain, default values not appropriate")
