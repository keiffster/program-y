import logging
import slixmpp

from programy.clients.clients import BotClient
from programy.config.client.xmpp import XmppClientConfiguration


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


if __name__ == '__main__':

    def run():
        logging.debug("Loading Xmpp client, please wait...")
        xmpp_app = XmppBotClient()
        xmpp_app.run()

    run()