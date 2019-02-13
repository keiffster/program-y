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

from programy.config.base import BaseConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BotSpellingConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="spelling")
        self._classname = None
        self._alphabet = None
        self._check_before = False
        self._check_and_retry = False

    @property
    def classname(self):
        return self._classname

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def check_before(self):
        return self._check_before

    @property
    def check_and_retry(self):
        return self._check_and_retry

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        spelling = configuration_file.get_section(self._section_name, configuration)
        if spelling is not None:
            self._classname = configuration_file.get_option(spelling, "classname", missing_value=None, subs=subs)
            self._alphabet = configuration_file.get_option(spelling, "alphabet", missing_value=None, subs=subs)
            self._check_before = configuration_file.get_bool_option(spelling, "check_before", missing_value=False, subs=subs)
            self._check_and_retry = configuration_file.get_bool_option(spelling, "check_and_retry", missing_value=False, subs=subs)
        else:
            YLogger.warning(self, "'spelling' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.spelling.norvig.NorvigSpellingChecker"
            data['alphabet'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            data['check_before'] = False
            data['check_and_retry'] = False
        else:
            data['classname'] = self._classname
            data['alphabet'] = self._alphabet
            data['check_before'] = self._check_before
            data['check_and_retry'] = self._check_and_retry
