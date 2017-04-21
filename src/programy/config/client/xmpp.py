"""
Copyright (c) 2016 Keith Sterling

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
from programy.config.client.client import ClientConfiguration

class XmppConfiguration(BaseConfigurationData):

    def __init__(self):
        self._server = None
        self._port = 5222
        self._xep_0030 = False
        self._xep_0004 = False
        self._xep_0060 = False
        self._xep_0199 = False
        BaseConfigurationData.__init__(self, "xmpp")

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def xep_0030(self):
        return self._xep_0030

    @property
    def xep_0004(self):
        return self._xep_0004

    @property
    def xep_0060(self):
        return self._xep_0060

    @property
    def xep_0199(self):
        return self._xep_0199

    def load_config_section(self, config_file, bot_root):
        xmpp = config_file.get_section(self.section_name)
        if xmpp is not None:
            self._server = config_file.get_option(xmpp, "server")
            self._port = config_file.get_int_option(xmpp, "port", missing_value=5222)
            self._xep_0030 = config_file.get_bool_option(xmpp, "xep_0030")
            self._xep_0004 = config_file.get_bool_option(xmpp, "xep_0004")
            self._xep_0060 = config_file.get_bool_option(xmpp, "xep_0060")
            self._xep_0199 = config_file.get_bool_option(xmpp, "xep_0199")

class XmppClientConfiguration(ClientConfiguration):

    def __init__(self):
        ClientConfiguration.__init__(self)
        self._xmpp_config = XmppConfiguration()

    @property
    def xmpp_configuration(self):
        return self._xmpp_config

    def load_config_data(self, config_file, bot_root):
        super(XmppClientConfiguration, self).load_config_data(config_file, bot_root)
        self._xmpp_config.load_config_section(config_file, bot_root)
