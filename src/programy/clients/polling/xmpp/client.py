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
import sleekxmpp

from programy.clients.client import BotClient
from programy.clients.polling.xmpp.config import XmppConfiguration
from programy.clients.polling.xmpp.xmpp import XmppClient


class XmppBotClient(BotClient):

    def __init__(self, argument_parser=None):
        self._xmpp_client = None
        BotClient.__init__(self, "XMPP", argument_parser)

    def get_description(self):
        return 'ProgramY AIML2.0 XMPP Client'

    def get_client_configuration(self):
        return XmppConfiguration()

    def get_username_password(self, license_keys):
        username = license_keys.get_key("XMPP_USERNAME")
        password = license_keys.get_key("XMPP_PASSWORD")
        return username, password

    def get_server_port(self, configuration):
        server = configuration.client_configuration.server
        port = configuration.client_configuration.port
        return server, port

    def create_client(self, username, password):
        return XmppClient(self, username, password)

    def ask_question(self, userid, question):
        response = self.bot.ask_question(userid, question, responselogger=self)
        return response

    def run(self):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("XMPP Client is running....")

        username, password = self.get_username_password(self.bot.license_keys)
        server, port = self.get_server_port(self.configuration)

        self._xmpp_client = self.create_client(username, password)
        self._xmpp_client.register_xep_plugins(self.configuration)
        self._xmpp_client.run(server, port, block=True)


if __name__ == '__main__':

    def run():
        print("Loading Xmpp client, please wait. See log output for progress...")
        xmpp_app = XmppBotClient()
        xmpp_app.run()

    run()
