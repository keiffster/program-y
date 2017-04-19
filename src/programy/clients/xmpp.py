import logging
import slixmpp

from programy.clients.clients import BotClient
from programy.config.client.xmpp import XmppClientConfiguration

class XmppClient(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()



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

        self._client = XmppClient(username, password)
        if self.configuration.xmpp_configuration.xep_0030 is True:
            self._client.register_plugin('xep_0030')
        if self.configuration.xmpp_configuration.xep_0004 is True:
            self._client.register_plugin('xep_0004')
        if self.configuration.xmpp_configuration.xep_0060 is True:
            self._client.register_plugin('xep_0060')
        if self.configuration.xmpp_configuration.xep_0199 is True:
            self._client.register_plugin('xep_0199')

        self._client.connect()
        self._client.process()

if __name__ == '__main__':

    def run():
        logging.debug("Loading Xmpp client, please wait...")
        xmpp_app = XmppBotClient()
        xmpp_app.run()

    run()