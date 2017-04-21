import logging
import sleekxmpp

from programy.clients.clients import BotClient
from programy.config.client.xmpp import XmppClientConfiguration

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

    def __init__(self, env="XMPP"):
        self._environment = env
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", self._environment])
        
    def get_client_configuration(self):
        return XmppClientConfiguration()

    def run(self):
        logging.debug("%s App Running.."%self._environment)

        username = self.bot.license_keys.get_key("XMPP_USERNAME")
        password = self.bot.license_keys.get_key("XMPP_PASSWORD")

        server = self.configuration.xmpp_configuration.server
        port = self.configuration.xmpp_configuration.port

        self._client = XmppClient(self, username, password)
        if self.configuration.xmpp_configuration.xep_0030 is True:
            self._client.register_plugin('xep_0030')
        if self.configuration.xmpp_configuration.xep_0004 is True:
            self._client.register_plugin('xep_0004')
        if self.configuration.xmpp_configuration.xep_0060 is True:
            self._client.register_plugin('xep_0060')
        if self.configuration.xmpp_configuration.xep_0199 is True:
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