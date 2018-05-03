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


class DebugFileConfiguration(BaseSectionConfigurationData):

    def __init__(self, name, filename=None, file_format="txt", encoding="utf-8", delete_on_start=False):
        BaseSectionConfigurationData.__init__(self, name)
        self._file = filename
        self._file_format = file_format
        self._encoding = encoding
        self._delete_on_start = delete_on_start

    @property
    def filename(self):
        return self._file

    @property
    def file_format(self):
        return self._file_format

    @property
    def encoding(self):
        return self._encoding

    @property
    def delete_on_start(self):
        return self._delete_on_start

    def load_config_section(self, configuration_file, configuration, bot_root):
        debugfile_config = configuration_file.get_option(configuration, self._section_name)
        if debugfile_config is not None:
            file = configuration_file.get_option(debugfile_config, "file", missing_value=None)
            if file is not None:
                self._file = self.sub_bot_root(file, bot_root)
            self._file_format = configuration_file.get_option(debugfile_config, "format", missing_value="txt")
            self._encoding = configuration_file.get_option(debugfile_config, "encoding", missing_value="utf-8")
            self._delete_on_start = configuration_file.get_bool_option(debugfile_config, "delete_on_start", missing_value=False)
        else:
            YLogger.warning(self, "'%s' section missing from aiml files config, using to defaults", self.section_name)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['file'] = "./%s.csv"%self.id
            data['file_format'] = "csv"
            data['encoding'] = 'utf-8'
            data['delete_on_start'] = True
        else:
            data['file'] = self._file
            data['file_format'] = self._file_format
            data['encoding'] = self._encoding
            data['delete_on_start'] = self._delete_on_start
