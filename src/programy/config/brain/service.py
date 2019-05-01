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

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainServiceConfiguration(BaseSectionConfigurationData):

    additionals = ['denied_srai']

    def __init__(self, service_name):
        BaseSectionConfigurationData.__init__(self, service_name)
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

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        service = configuration_file.get_section(self.section_name, configuration)
        if service is not None:
            self._classname = configuration_file.get_option(service, "classname", missing_value=None, subs=subs)
            self._method = configuration_file.get_option(service, "method", missing_value=None, subs=subs)
            self._host = configuration_file.get_option(service, "host", missing_value=None, subs=subs)
            self._port = configuration_file.get_int_option(service, "port", missing_value=None, subs=subs)
            self._url = configuration_file.get_option(service, "url", missing_value=None, subs=subs)
            self.load_additional_key_values(configuration_file, service)
        else:
            YLogger.warning(self, "'services' section missing from brain config, using to defaults")

    def to_yaml(self, data, defaults=True):
        data['classname'] = self._classname
        data['method'] = self._method
        data['host'] = self._host
        data['port'] = self._port
        data['url'] = self._url
