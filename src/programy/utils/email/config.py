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


class EmailConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="email")
        self._host      = None
        self._port      = None
        self._username  = None
        self._password  = None
        self._from_addr  = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def from_addr(self):
        return self._from_addr

    def check_for_license_keys(self, license_keys):
        self._username = self._extract_license_key(self._username, license_keys)
        self._password = self._extract_license_key(self._password, license_keys)
        BaseConfigurationData.check_for_license_keys(license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        email = configuration_file.get_section(self._section_name, configuration)
        if email is not None:
            self._host = configuration_file.get_option(email, "host", missing_value=None)
            self._port = configuration_file.get_option(email, "port", missing_value=None)
            self._username = configuration_file.get_option(email, "username", missing_value=None)
            self._password = configuration_file.get_option(email, "password", missing_value=None)
            self._from_addr = configuration_file.get_option(email, "from_addr", missing_value=None)
            if self._from_addr is None:
                self._from_addr = self._username
        else:
            YLogger.warning(self, "'email' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['host'] = None
            data['port'] = None
            data['username'] = None
            data['password'] = None
            data['from_addr'] = None
        else:
            data['host'] = self._host
            data['port'] = self._port
            data['username'] = self._username
            data['password'] = self._password
            data['from_addr'] = self._from_addr
