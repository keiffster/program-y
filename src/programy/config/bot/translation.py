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


class BotTranslatorConfiguration(BaseConfigurationData):

    def __init__(self, name):
        BaseConfigurationData.__init__(self, name=name)
        self._classname = None
        self._from_lang = None
        self._to_lang = None

    @property
    def classname(self):
        return self._classname

    @property
    def from_lang(self):
        return self._from_lang

    @property
    def  to_lang(self):
        return self._to_lang

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        translation = configuration_file.get_section(self._section_name, configuration)
        if translation is not None:
            self._classname = configuration_file.get_option(translation, "classname", missing_value=None, subs=subs)
            self._from_lang = configuration_file.get_option(translation, "from", missing_value=None, subs=subs)
            self._to_lang = configuration_file.get_option(translation, "to", missing_value=None, subs=subs)
        else:
            YLogger.warning(self, "'translation' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.translation.textblob.TextBlobTranslator"
            data['from'] = None
            data['to'] = None
        else:
            data['classname'] = self._classname
            data['from'] = self._from_lang
            data['to'] = self._to_lang
