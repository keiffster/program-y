"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging

from programy.config.base import BaseSectionConfigurationData


class BrainLanguageConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "language")
        self._english = True
        self._chinese = False

    @property
    def english(self):
        return self._english

    @property
    def chinese(self):
        return self._chinese

    def load_config_section(self, configuration_file, configuration, bot_root):
        language = configuration_file.get_section(self._section_name, configuration)
        if language is not None:
            self._english = configuration_file.get_bool_option(language, "english", missing_value=True)
            self._chinese = configuration_file.get_bool_option(language, "chinese", missing_value=True)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("'language' section missing from brain config, using to defaults")
