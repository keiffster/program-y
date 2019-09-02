import unittest

from programy.dialog.question import Question, Sentence
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from programytest.client import TestClient


class TemplateGraphClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TemplateGraphClient, self).load_storage()
        self.add_default_stores()
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()


class TemplateGraphTestClient(unittest.TestCase):

    def create_client_context(self, testid):
        client = TemplateGraphClient()
        return client.create_client_context(testid)

    def setUp(self):

        self._client = TemplateGraphClient()
        self._client_context = self._client.create_client_context("testid")

        self._graph = self._client_context.bot.brain.aiml_parser.template_parser

        self.test_sentence = Sentence(self._client_context, "test sentence")

        test_node = PatternOneOrMoreWildCardNode("*")

        self.test_sentence._matched_context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        self.test_sentence._matched_context._matched_nodes = [Match(Match.WORD, test_node, 'one'),
                                                              Match(Match.WORD, test_node, 'two'),
                                                              Match(Match.WORD, test_node, 'three'),
                                                              Match(Match.WORD, test_node, 'four'),
                                                              Match(Match.WORD, test_node, 'five'),
                                                              Match(Match.WORD, test_node, 'six'),
                                                              Match(Match.TOPIC, test_node, '*'),
                                                              Match(Match.THAT, test_node, '*')]

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_sentence(self.test_sentence)
        conversation._questions.append(question)
