import os

from programy.clients.events.console.client import ConsoleBotClient


class ProgramYChatbot(ConsoleBotClient):

    def __init__(self, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)

    def parse_configuration(self):
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = \
            [os.path.dirname(__file__)]

if __name__ == '__main__':

    print ("Running ProgramY Chatbot with default options....")

    chatbot = ProgramYChatbot()
    chatbot.run()


