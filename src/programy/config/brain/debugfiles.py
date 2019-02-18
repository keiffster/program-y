
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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
import os

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainDebugFilesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "debugfiles")
        self._save_errors = False
        self._save_duplicates = False

    @property
    def save_errors(self):
        return self._save_errors

    @property
    def save_duplicates(self):
        return self._save_duplicates

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        debugfiles = configuration_file.get_section("debugfiles", configuration)
        if debugfiles is not None:
            self._save_errors = configuration_file.get_bool_option(debugfiles, "save-errors", missing_value=False, subs=subs)
            self._save_duplicates = configuration_file.get_bool_option(debugfiles, "save-duplicates", missing_value=False, subs=subs)
        else:
            YLogger.warning(self, "'debugfiles' section missing from brain config, using debugfile defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['save_errors'] = False
            data['save_duplicates'] = False
        else:
            data['save_errors'] = self._save_errors
            data['save_duplicates'] = self._save_duplicates
