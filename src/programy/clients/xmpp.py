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
import sleekxmpp

from programy.clients.client import BotClient
from programy.config.sections.client.xmpp import XmppConfiguration

class XmppClient(sleekxmpp.ClientXMPP):

    def __init__(self, bot_client, jid, password):
        self.bot_client = bot_client
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):

            question = msg['body']
            userid = msg['from']

            response =  self.bot_client.bot.ask_question(userid, question)

            msg.reply(response).send()


class XmppBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, argument_parser)

    def set_environment(self, env='xmpp'):
        self.bot.brain.predicates.pairs.append(["env", env])
        
    def get_client_configuration(self):
        return XmppConfiguration()

    def run(self):
        logging.debug("%s App Running.."%self.bot.brain.predicates.predicate("env"))

        username = self.bot.license_keys.get_key("XMPP_USERNAME")
        password = self.bot.license_keys.get_key("XMPP_PASSWORD")

        server = self.configuration.client_configuration.server
        port = self.configuration.client_configuration.port

        self._client = XmppClient(self, username, password)
        if self.configuration.client_configuration.xep_0030 is True:
            self._client.register_plugin('xep_0030')
        if self.configuration.client_configuration.xep_0004 is True:
            self._client.register_plugin('xep_0004')
        if self.configuration.client_configuration.xep_0060 is True:
            self._client.register_plugin('xep_0060')
        if self.configuration.client_configuration.xep_0199 is True:
            self._client.register_plugin('xep_0199')

        if self._client.connect((server, port)):
            print("Connected, running...")
            self._client.process(block=True)
        else:
            print("Failed to connect, exiting...")

if __name__ == '__main__':

    def run():
        print("Loading Xmpp client, please wait. See log output for progress...")
        xmpp_app = XmppBotClient()
        xmpp_app.run()

    run()