import unittest
import datetime

from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.client import TestClient


class MatcherTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MatcherTestClient, self).load_storage()
        self.add_default_stores()
        self.add_pattern_nodes_store()
        

class MatchContextTests(unittest.TestCase):

    def setUp(self):
        client = MatcherTestClient()
        self._client_context = client.create_client_context("testid")

    def test_match_context_depth(self):
        context1 = MatchContext(max_search_depth=100, max_search_timeout=60)
        self.assertEqual(100, context1.max_search_depth)
        self.assertEqual(60, context1.max_search_time)

    def test_match_context_depth(self):
        context = MatchContext(max_search_depth=100, max_search_timeout=60)
        self.assertEqual(100, context.max_search_depth)
        self.assertEqual(60, context.max_search_timeout)
        self.assertFalse(context.matched())
        template = PatternTemplateNode(template=TemplateNode())
        context.template_node = template
        self.assertIsNotNone(context.template_node)
        self.assertTrue(context.matched())

    def test_match_context_pop_push(self):
        topic = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=60)
        self.assertEqual(0, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(1, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(2, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(3, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(2, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(1, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(0, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(0, len(context.matched_nodes))

    def test_match_context_star(self):
        word = PatternOneOrMoreWildCardNode("*")
        topic = PatternOneOrMoreWildCardNode("*")
        that = PatternOneOrMoreWildCardNode("*")

        context = MatchContext(max_search_depth=100, max_search_timeout=60)

        context.add_match(Match(Match.WORD, word, "Hello"))
        context.add_match(Match(Match.TOPIC, topic, "Hello Topic"))
        context.add_match(Match(Match.THAT, that, "Hello That"))
        self.assertEqual(3, len(context.matched_nodes))

        self.assertEqual("Hello", context.star(self._client_context, 1))
        self.assertIsNone(context.star(self._client_context, 2))
        self.assertEqual("Hello Topic", context.topicstar(self._client_context, 1))
        self.assertIsNone(context.topicstar(self._client_context, 2))
        self.assertEqual("Hello That", context.thatstar(self._client_context, 1))
        self.assertIsNone(context.thatstar(self._client_context, 2))

    def test_time_functions(self):
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        self.assertEqual(-1, context.max_search_timeout)
        self.assertFalse(context.search_time_exceeded())

        context = MatchContext(max_search_depth=100, max_search_timeout=0)
        self.assertEqual(0, context.max_search_timeout)
        self.assertTrue(context.search_time_exceeded())

        context = MatchContext(max_search_depth=100, max_search_timeout=60)
        time_now = datetime.datetime.now()
        prev_time = time_now - datetime.timedelta(seconds=-70)
        context._total_search_start = prev_time
        self.assertTrue(context.search_time_exceeded())

    def test_to_json(self):
        topic = PatternOneOrMoreWildCardNode("*")
        word1 = PatternWordNode("Hi")
        word2 = PatternWordNode("There")
        context = MatchContext(max_search_depth=100, max_search_timeout=60,
                               template_node=PatternTemplateNode(TemplateWordNode("Hello")))
        context.add_match(Match(Match.TOPIC, topic, None))
        context.add_match(Match(Match.WORD, word1, "Hi"))
        context.add_match(Match(Match.WORD, word2, "There"))

        json_data = context.to_json()

        self.assertIsNotNone(json_data)
        self.assertEquals(json_data["max_search_depth"], 100)
        self.assertEquals(json_data["max_search_timeout"], 60)
        self.assertIsInstance(json_data["total_search_start"], datetime.datetime)

        self.assertEquals(3, len(json_data["matched_nodes"]))
        self.assertEquals(json_data["matched_nodes"][0], {'multi_word': True,
                                                          'node': 'ONEORMORE [*]',
                                                          'type': 'Topic',
                                                          'wild_card': True,
                                                          'words': []})
        self.assertEquals(json_data["matched_nodes"][1], {'multi_word': False,
                                                         'node': 'WORD [Hi]',
                                                         'type': 'Word',
                                                         'wild_card': False,
                                                         'words': ["Hi"]})
        self.assertEquals(json_data["matched_nodes"][2], {'multi_word': False,
                                                         'node': 'WORD [There]',
                                                         'type': 'Word',
                                                         'wild_card': False,
                                                         'words': ["There"]})

    def test_from_json(self):
        json_data = {'max_search_depth': 100,
                     'max_search_timeout': 60,
                     'total_search_start': datetime.datetime(2019, 8, 29, 17, 25, 7, 141098),
                     'sentence': 'Hello',
                     'response': 'Hi there',
                     'matched_nodes': [{'type': 'Topic', 'node': 'ONEORMORE [*]', 'words': [], 'multi_word': True, 'wild_card': True},
                                       {'type': 'Word', 'node': 'WORD [Hi]', 'words': ['Hi'], 'multi_word': False, 'wild_card': False},
                                       {'type': 'Word', 'node': 'WORD [There]', 'words': ['There'], 'multi_word': False, 'wild_card': False}]
                     }

        match_context = MatchContext.from_json(json_data)
        self.assertIsNotNone(match_context)
        self.assertEquals(match_context._max_search_depth, 100)
        self.assertEquals(match_context._max_search_timeout, 60)
        self.assertIsInstance(match_context._total_search_start, datetime.datetime)
        self.assertEquals(match_context.template_node, None)
        self.assertEquals(match_context.sentence, "Hello")
        self.assertEquals(match_context.response, "Hi there")
        self.assertEquals(3, len(match_context._matched_nodes))
