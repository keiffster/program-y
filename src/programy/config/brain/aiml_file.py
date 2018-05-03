"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
from programy.utils.logging.ylogger import YLogger

from programy.config.brain.file import BrainFileConfiguration
from programy.config.brain.debugfile import DebugFileConfiguration


class BrainAIMLFileConfiguration(BrainFileConfiguration):

    def __init__(self, name="aiml"):
        BrainFileConfiguration.__init__(self, name, extension="aiml", directories=False)
        self._errors = None
        self._duplicates = None
        self._conversation = None

    @property
    def errors(self):
        return self._errors

    @property
    def duplicates(self):
        return self._duplicates

    @property
    def conversation(self):
        return self._conversation

    def load_config_section(self, configuration_file, configuration, bot_root):
        files_config = configuration_file.get_option(configuration, self.section_name)
        if files_config is not None:
            files = configuration_file.get_multi_file_option(files_config, "files", bot_root)
            if files is not None and files:
                self._files = files
                self._extension = configuration_file.get_option(files_config, "extension")
                self._directories = configuration_file.get_option(files_config, "directories")
            else:
                file = configuration_file.get_option(files_config, "file")
                if file is not None:
                    self._file = self.sub_bot_root(file, bot_root)

            self._errors = self.get_debug_file_configuration(configuration_file, files_config, "errors", bot_root)
            self._duplicates = self.get_debug_file_configuration(configuration_file, files_config, "duplicates", bot_root)
            self._conversation = self.get_debug_file_configuration(configuration_file, files_config, "conversation", bot_root)

        else:
            YLogger.warning(self, "'%s' section missing from bot config, using to defaults", self.section_name)

    def get_debug_file_configuration(self, configuration_file, files_config, debug_name, bot_root):
        keys = configuration_file.get_keys(files_config)
        if debug_name in keys:
            section = configuration_file.get_section(debug_name, files_config)
            if configuration_file.is_string(section):
                debug_config = configuration_file.get_option(files_config, debug_name, missing_value=None)
                if debug_config is not None:
                    filename = self.sub_bot_root(debug_config, bot_root)
                    return DebugFileConfiguration(debug_name, filename=filename)
            else:
                debug_file = DebugFileConfiguration(debug_name)
                debug_file.load_config_section(configuration_file, files_config, bot_root)
                return debug_file
        return None

    def to_yaml(self, data, defaults=True):
        self.config_to_yaml(data, DebugFileConfiguration('errors'), defaults)
        self.config_to_yaml(data, DebugFileConfiguration('duplicates'), defaults)
        self.config_to_yaml(data, DebugFileConfiguration('conversation'), defaults)
