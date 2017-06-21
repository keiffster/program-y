import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config.client.client import ClientConfiguration
from programy.config.brain import BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.pattern.matcher import MatchContext, Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.aiml_parser import AIMLParser

class TemplateGraphTestClient(unittest.TestCase):

    def setUp(self):
        self.parser = TemplateGraph(AIMLParser())
        self.assertIsNotNone(self.parser)

        self.test_brain = None
        self.test_sentence = Sentence("test sentence")

        test_node = PatternOneOrMoreWildCardNode("*")

        self.test_sentence._matched_context = MatchContext()
        self.test_sentence._matched_context._matched_nodes = [Match(Match.WORD, test_node, 'one'),
                                                             Match(Match.WORD, test_node, 'two'),
                                                             Match(Match.WORD, test_node, 'three'),
                                                             Match(Match.WORD, test_node, 'four'),
                                                             Match(Match.WORD, test_node, 'five'),
                                                             Match(Match.WORD, test_node, 'six'),
                                                             Match(Match.TOPIC, test_node, '*'),
                                                             Match(Match.THAT, test_node, '*')]

        test_config = ClientConfiguration()

        self.test_bot = Bot(Brain(BrainConfiguration()), config=test_config.bot_configuration)
        self.test_clientid = "testid"

        conversation = self.test_bot.get_conversation(self.test_clientid)
        question = Question.create_from_sentence(self.test_sentence)
        conversation._questions.append(question)
