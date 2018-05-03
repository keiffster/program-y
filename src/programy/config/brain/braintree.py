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


class BrainBraintreeConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "braintree")
        self._file = None
        self._content = None

    @property
    def file(self):
        return self._file

    @property
    def content(self):
        return self._content

    def load_config_section(self, configuration_file, configuration, bot_root):
        braintree = configuration_file.get_section("braintree", configuration)
        if braintree is not None:
            file = configuration_file.get_option(braintree, "file", missing_value=None)
            if file is not None:
                self._file = self.sub_bot_root(file, bot_root)
            self._content = configuration_file.get_option(braintree, "content", missing_value="txt")
        else:
            YLogger.warning(self, "'braintree' section missing from bot config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['file'] = "./braintree.xml"
            data['content'] = "xml"
        else:
            data['file'] = self._file
            data['content'] = self._content
