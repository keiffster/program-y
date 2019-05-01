"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.config.container import BaseContainerConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class PingResponderConfig(BaseContainerConfigurationData):

    def __init__(self, name="responder"):
        BaseContainerConfigurationData.__init__(self, name)
        self._name = "Client Ping Responder"
        self._host = None
        self._port = None
        self._url = None
        self._shutdown = None
        self._register = None
        self._unregister = None

    @property
    def name(self):
        return self._name

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    @property
    def shutdown(self):
        return self._shutdown

    @property
    def register(self):
        return self._register

    @property
    def unregister(self):
        return self._unregister

    def load_config_section(self, configuration_file, section, bot_root, subs: Substitutions = None):
        triggers = configuration_file.get_section(self._section_name, section)
        if triggers is not None:
            self._name = configuration_file.get_option(triggers, "name")
            self._host = configuration_file.get_option(triggers, "host")
            self._port = configuration_file.get_option(triggers, "port")
            self._url = configuration_file.get_option(triggers, "url")
            self._shutdown = configuration_file.get_option(triggers, "shutdown")
            self._register = configuration_file.get_option(triggers, "register")
            self._unregister = configuration_file.get_option(triggers, "unregister")

        else:
            YLogger.warning(self, "'responder' section missing from client config, using defaults")

    def to_yaml(self, data, defaults=True):

        assert (data is not None)

        if defaults is True:
            data['name'] = "Client Ping Responder"
            data['host'] = None
            data['port'] = None
            data['url'] = None
            data['shutdown'] = None
            data['register'] = None
            data['unregister'] = None

        else:
            data['name'] = self._name
            data['host'] = self._host
            data['port'] = self._port
            data['url'] = self._url
            data['shutdown'] = self._shutdown
            data['register'] = self._register
            data['unregister'] = self._unregister
