"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation dirs (the "Software"), to deal in the Software without restriction, including without limitation
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
from programy.utils.substitutions.substitues import Substitutions


class FileStoreConfiguration(BaseSectionConfigurationData):
    
    def __init__(self, name='storage', dirs=None, extension=None, subdirs=False, format=None, encoding=None, delete_on_start=False, file=None):
        BaseSectionConfigurationData.__init__(self, name)

        self._dirs = None
        self._has_single_file = False

        if dirs is not None:
            if isinstance(dirs, (list,)) is False:
                self._dirs = [dirs]
                self._has_single_file = True
            else:
                self._dirs = dirs[:]
                self._has_single_file = False
        elif file is not None:
            self._dirs = [file]
            self._has_single_file = True

        self._extension = extension
        self._subdirs = subdirs

        self._format = format
        self._encoding = encoding
        
        self._delete_on_start = delete_on_start

    def has_multiple_dirs(self):
        if self._has_single_file:
            return False
        else:
            return True

    def has_single_file(self):
        return self._has_single_file

    @property
    def file(self):
        return self._dirs[0]

    @property
    def dirs(self):
        return self._dirs

    @property
    def extension(self):
        return self._extension

    @property
    def subdirs(self):
        return self._subdirs

    @property
    def format(self):
        return self._format

    @property
    def encoding(self):
        return self._encoding

    @property
    def delete_on_start(self):
        return self._delete_on_start

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        dirs_config = configuration_file.get_option(configuration, self.section_name)
        if dirs_config is not None:
            self.extract_configuration(configuration_file, dirs_config, bot_root, subs=subs)
        else:
            YLogger.warning(self, "'%s' section missing from bot config, using to defaults", self.section_name)

    def extract_configuration(self, configuration_file, files_config, bot_root, subs: Substitutions = None):
        dirs = configuration_file.get_multi_file_option(files_config, "dirs", bot_root, subs=subs)
        if dirs is not None and dirs:
            self._dirs = dirs
            self._extension = configuration_file.get_option(files_config, "extension", subs=subs)
            self._subdirs = configuration_file.get_bool_option(files_config, "subdirs", False, subs=subs)
            self._has_single_file = False
        else:
            file = configuration_file.get_option(files_config, "file", subs=subs)
            if file is not None:
                self._dirs = [self.sub_bot_root(file, bot_root)]
                self._has_single_file = True

        self._format = configuration_file.get_option(files_config, "format", None, subs=subs)
        self._encoding = configuration_file.get_option(files_config, "encoding", None, subs=subs)

        self._delete_on_start = configuration_file.get_bool_option(files_config, "delete_on_start", False, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['dirs'] = "./storage/%s"%self.id
            data['extension'] = ".txt"
            data['subdirs'] = False

            data['file'] = None

            data['format'] = None
            data['encoding'] = None
            data['delete_on_start'] = False
        else:
            data['dirs'] = self._dirs
            data['extension'] = self._extension
            data['subdirs'] = self._subdirs

            data['file'] = None

            data['format'] = self._format
            data['encoding'] = self._encoding
            data['delete_on_start'] = self._delete_on_start
