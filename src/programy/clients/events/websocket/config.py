"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without WebSocketriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.config.client.config import ClientConfigurationData


class WebSocketConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "webwebsocket")
        self._host = "0.0.0.0"
        self._port = 80

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def load_configuration(self, configuration_file, bot_root):
        websocket = configuration_file.get_section(self.section_name)
        if websocket is not None:
            self._host = configuration_file.get_option(websocket, "host", missing_value="0.0.0.0")
            self._port = configuration_file.get_option(websocket, "port", missing_value=80)
        super(WebSocketConfiguration, self).load_configuration(configuration_file, websocket, bot_root)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['host'] = "0.0.0.0"
            data['port'] = 80
        else:
            data['host'] = self._host
            data['port'] = self._port

        super(WebSocketConfiguration, self).to_yaml(data, defaults)