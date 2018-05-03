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

from programy.config.section import BaseSectionConfigurationData


class BrainFileConfiguration(BaseSectionConfigurationData):

    def __init__(self, name="files", files=None, file=None, extension=None, directories=False):
        BaseSectionConfigurationData.__init__(self, name)
        if files is None:
            self._files = []
        else:
            self._files = files
        self._file = file
        self._extension = extension
        self._directories = directories

    def has_multiple_files(self):
        return bool(self._files is not None and self._files)

    def has_single_file(self):
        return bool(self._file is not None)

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
        else:
            YLogger.warning(self, "'%s' section missing from bot config, using to defaults", self.section_name)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['files'] = "./%s"%self.id
            data['extension'] = ".txt"
            data['directories'] = False
        else:
            data['files'] = self._files
            data['extension'] = self._extension
            data['directories'] = self._directories
