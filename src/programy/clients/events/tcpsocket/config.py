"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without Socketriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class SocketConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "socket")
        self._host = "0.0.0.0"
        self._port = 80
        self._debug = False
        self._queue = 5
        self._max_buffer = 1024

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def debug(self):
        return self._debug

    @property
    def queue(self):
        return self._queue

    @property
    def max_buffer(self):
        return self._max_buffer

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, socket, bot_root, subs: Substitutions = None):
        if socket is not None:
            self._host = configuration_file.get_option(socket, "host", missing_value="0.0.0.0", subs=subs)
            self._port = configuration_file.get_option(socket, "port", missing_value=80, subs=subs)
            self._debug = configuration_file.get_bool_option(socket, "debug", missing_value=False, subs=subs)
            self._workers = configuration_file.get_option(socket, "queue", missing_value=5, subs=subs)
            self._max_buffer = configuration_file.get_option(socket, "max_buffer", missing_value=1024, subs=subs)
            super(SocketConfiguration, self).load_configuration_section(configuration_file, socket, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['host'] = "0.0.0.0"
            data['port'] = 80
            data['debug'] = False
            data['queue'] = 5
            data['max_buffer'] = 1024
        else:
            data['host'] = self._host
            data['port'] = self._port
            data['debug'] = self._debug
            data['queue'] = self._queue
            data['max_buffer'] = self._max_buffer

        super(SocketConfiguration, self).to_yaml(data, defaults)