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
from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class XmppConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "xmpp")
        self._server = None
        self._port = 5222
        self._xep_0030 = False
        self._xep_0004 = False
        self._xep_0060 = False
        self._xep_0199 = False

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

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, xmpp, bot_root, subs: Substitutions = None):
        if xmpp is not None:
            self._server = configuration_file.get_option(xmpp, "server", subs=subs)
            self._port = configuration_file.get_int_option(xmpp, "port", missing_value=5222, subs=subs)
            self._xep_0030 = configuration_file.get_bool_option(xmpp, "xep_0030", subs=subs)
            self._xep_0004 = configuration_file.get_bool_option(xmpp, "xep_0004", subs=subs)
            self._xep_0060 = configuration_file.get_bool_option(xmpp, "xep_0060", subs=subs)
            self._xep_0199 = configuration_file.get_bool_option(xmpp, "xep_0199", subs=subs)
            super(XmppConfiguration, self).load_configuration_section(configuration_file, xmpp, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['server'] = "talk.google.com"
            data['port'] = 5222
            data['xep_0030'] = True
            data['xep_0004'] = True
            data['xep_0060'] = True
            data['xep_0199'] = True
        else:
            data['server'] = self._server
            data['port'] = self._port
            data['xep_0030'] = self._xep_0030
            data['xep_0004'] = self._xep_0004
            data['xep_0060'] = self._xep_0060
            data['xep_0199'] = self._xep_0199

        super(XmppConfiguration, self).to_yaml(data, defaults)