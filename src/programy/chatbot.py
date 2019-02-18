import os

from programy.clients.events.console.client import ConsoleBotClient
from programy.utils.text.dateformat import DateFormatter
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.programy import ProgramyConfiguration

class ProgramYChatbot(ConsoleBotClient):

    def __init__(self, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)

    def load_configuration(self, arguments):

        category_path = os.path.dirname(__file__)
        pattern_path = os.path.dirname(__file__) + os.sep + "parser/pattern/pattern_nodes.conf"
        template_path = os.path.dirname(__file__) + os.sep + "parser/template/template_nodes.conf"

        client_config = self.get_client_configuration()
        self._configuration = ProgramyConfiguration(client_config)

        yaml_file = YamlConfigurationFile()
        yaml_file.load_from_text("""
console:
  description: Program-Y Console Client
  bot:  bot
  prompt: ">>>"

  storage:
      entities:
          categories: file
          template_nodes: file
          pattern_nodes: file

      stores:

          file:
              type:   file
              config:
                categories_storage:
                  dirs: %s
                  subdirs: true
                  extension: .aiml

                pattern_nodes_storage:
                  file: %s
                template_nodes_storage:
                  file: %s

#####################################################################################################
#

bot:
    brain: brain

    initial_question: Hi, how can I help you today?
    default_response: Sorry, I don't have an answer for that!
    exit_response: So long, and thanks for the fish!

    override_properties: true

        """%(category_path, pattern_path, template_path), client_config, ".")

    def add_local_properties(self):
        client_context = self.create_client_context("console")
        client_context.brain.properties.add_property("name", "ProgramY")
        client_context.brain.properties.add_property("app_version", "1.0.0")
        client_context.brain.properties.add_property("grammar_version", "1.0.0")
        date_formatter = DateFormatter()
        client_context.brain.properties.add_property("birthdate", date_formatter.locate_appropriate_date_time())

if __name__ == '__main__':

    print ("Running ProgramY Chatbot with default options....")

    chatbot = ProgramYChatbot()

    chatbot.add_local_properties()

    chatbot.run()


