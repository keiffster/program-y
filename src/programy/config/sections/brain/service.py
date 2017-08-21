"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.config.base import BaseConfigurationData

class BrainServiceConfiguration(BaseConfigurationData):

    additionals = ['denied_srai']

    def __init__(self, service_name):
        BaseConfigurationData.__init__(self, service_name)
        self._classname = None
        self._method = None
        self._host = None
        self._port = None
        self._url = None

    @property
    def classname(self):
        return self._classname

    @property
    def method(self):
        return self._method

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    def additionals_to_add(self):
        return BrainServiceConfiguration.additionals

    def load_config_section(self, file_config, service_config, bot_root):
        service = file_config.get_section(self.section_name, service_config)
        if service is not None:
            self._classname = file_config.get_option(service, "classname", missing_value=None)
            self._method = file_config.get_option(service, "method", missing_value=None)
            self._host = file_config.get_option(service, "host", missing_value=None)
            self._port = file_config.get_option(service, "port", missing_value=None)
            self._url = file_config.get_option(service, "url", missing_value=None)
            self.load_additional_key_values(file_config, service)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning("'services' section missing from brain config, using to defaults")
