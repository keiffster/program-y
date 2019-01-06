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
import sleekxmpp

class XmppClient(sleekxmpp.ClientXMPP):

    def __init__(self, bot_client, jid, password):
        self._bot_client = bot_client
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handlers()

    def add_event_handlers(self):
        YLogger.debug(self, "XMPPClient adding event handlers")
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def register_xep_plugins(self, configuration):
        YLogger.debug(self, "XMPPClient registering XEP plugins")

        if configuration.xep_0030 is True:
            YLogger.debug(self, "XMPPClient registering xep_0030 plugin")
            self.register_plugin('xep_0030')

        if configuration.xep_0004 is True:
            YLogger.debug(self, "XMPPClient registering xep_0004 plugin")
            self.register_plugin('xep_0004')

        if configuration.xep_0060 is True:
            YLogger.debug(self, "XMPPClient registering xep_0060 plugin")
            self.register_plugin('xep_0060')

        if configuration.xep_0199 is True:
            YLogger.debug(self, "XMPPClient registering xep_0199 plugin")
            self.register_plugin('xep_0199')

    def start(self, event):
        YLogger.debug(self, "XMPPClient starting....")
        self.send_presence()
        self.get_roster()

    def is_valid_message(self, msg):
        return bool(msg['type'] in ('chat', 'normal'))

    def get_question(self, msg):
        return msg['body']

    def get_userid(self, msg):
        return msg['from'].bare

    def send_response(self, msg, response):
        if response is not None:
            msg.reply(response).send()

    def message(self, msg):
        if self.is_valid_message(msg) is True:

            question = self.get_question(msg)
            if question is None:
                YLogger.debug(self, "XMPPClient - Missing 'question' from XMPP message")
                return

            userid = self.get_userid(msg)
            if userid is None:
                YLogger.debug(self, "XMPCLient - Missing 'userid' from XMPP message")
                return

            response = self._bot_client.ask_question(userid, question)

            self.send_response(msg, response)

        else:
            YLogger.debug(self, "Invalid XMPP message")
            self.send_response(msg, "Sorry, no idea!")
