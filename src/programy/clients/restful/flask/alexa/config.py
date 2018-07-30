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
import logging

from programy.clients.restful.config import RestConfiguration


class AlexaConfiguration(RestConfiguration):

    def __init__(self):
        RestConfiguration.__init__(self, "alexa")
        self._ask_debug_level = logging.ERROR

    @property
    def ask_debug_level(self):
        return self._ask_debug_level

    def load_configuration(self, configuration_file, bot_root):
        alexa = configuration_file.get_section(self.section_name)
        if alexa is not None:
            self._ask_debug_level = configuration_file.get_option(alexa, "ask_debug_level", missing_value=logging.ERROR)
        super(AlexaConfiguration, self).load_configuration(configuration_file, bot_root)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['ask_debug_level'] = logging.ERROR
        else:
            data['ask_debug_level'] = self._ask_debug_level

        super(AlexaConfiguration, self).to_yaml(data, defaults)
