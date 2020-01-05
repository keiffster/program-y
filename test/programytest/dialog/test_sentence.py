import datetime
import unittest

from programy.dialog.sentence import Sentence
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.client import TestClient


class SentenceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("test1")

    def test_split_into_words1(self):
        self.assertEqual([], Sentence._split_into_words(self._client_context.brain.tokenizer, []))

    def test_split_into_words2(self):
        self.assertEqual([], Sentence._split_into_words(self._client_context.brain.tokenizer, None))

    def test_split_into_words3(self):
        self.assertEqual([], Sentence._split_into_words(None, "word1"))

    def test_split_into_words4(self):
        self.assertEqual([], Sentence._split_into_words(None, None))

    def test_split_into_words5(self):
        self.assertEqual(["word1"], Sentence._split_into_words(self._client_context.brain.tokenizer, "word1"))

    def test_split_into_words6(self):
        self.assertEqual(["word1", "word2", "word3"], Sentence._split_into_words(self._client_context.brain.tokenizer,
                                                                             "word1 word2 word3"))

    def test_sentence_creation_empty(self):
        sentence = Sentence(self._client_context, "")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(0)

    def test_sentence_creation_spaces(self):
        sentence = Sentence(self._client_context, " ")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(0)

    def test_split_into_words(self):
        sentence = Sentence(self._client_context, "HELLO")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())
        self.assertEqual("HELLO", sentence.word(0))
        self.assertEqual("HELLO", sentence.words_from_current_pos(self._client_context, 0))
        with self.assertRaises(Exception):
            sentence.sentence.word(1)
        self.assertEqual("HELLO", sentence.text(self._client_context))

    def test_sentence_creation_one_word(self):
        sentence = Sentence(self._client_context, "One")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(1)
        self.assertEqual("One", sentence.text(self._client_context))

    def test_sentence_creation_two_words(self):

        sentence = Sentence(self._client_context, "One Two")
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())
        self.assertEqual("One", sentence.word(0))
        self.assertEqual("Two", sentence.word(1))
        with self.assertRaises(Exception):
            sentence.sentence.word(2)
        self.assertEqual("One Two", sentence.text(self._client_context))

    def test_sentence_creation_two_words_diff_split_char(self):
        self._client_context.brain.tokenizer.split_chars = ","
        sentence = Sentence(self._client_context, "One,Two")
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())
        self.assertEqual("One", sentence.word(0))
        self.assertEqual("Two", sentence.word(1))
        with self.assertRaises(Exception):
            sentence.sentence.word(2)
        self.assertEqual("One,Two", sentence.text(self._client_context))

    def test_words_from_current_pos(self):
        sentence = Sentence(self._client_context, "One Two Three")
        self.assertIsNotNone(sentence)
        self.assertEqual("One Two Three", sentence.words_from_current_pos(self._client_context, 0))
        self.assertEqual("Two Three", sentence.words_from_current_pos(self._client_context, 1))
        self.assertEqual("Three", sentence.words_from_current_pos(self._client_context, 2))
        with self.assertRaises(Exception):
            self.assertEqual("Three", sentence.words_from_current_pos(self._client_context, 3))
        self.assertEqual("One Two Three", sentence.text(self._client_context))

    def test_to_json(self):

        topic = PatternOneOrMoreWildCardNode("*")
        word1 = PatternWordNode("Hi")
        word2 = PatternWordNode("There")
        context = MatchContext(max_search_depth=100, max_search_timeout=60,
                               template_node=PatternTemplateNode(TemplateWordNode("Hello")))
        context.add_match(Match(Match.TOPIC, topic, None))
        context.add_match(Match(Match.WORD, word1, "Hi"))
        context.add_match(Match(Match.WORD, word2, "There"))

        sentence = Sentence(self._client_context, "One Two Three", matched_context=context)

        json_data = sentence.to_json()
        self.assertIsNotNone(json_data)

    def test_from_json(self):

        json_data = {'words': ['One', 'Two', 'Three'],
                     'response': "Hello",
                     'positivity': 0.0,
                     'subjectivity': 0.5,
                     'matched_context': {'max_search_depth': 100,
                                         'max_search_timeout': 60,
                                         'total_search_start': datetime.datetime(2019, 8, 30, 7, 36, 54, 928185).strftime("%d/%m/%Y, %H:%M:%S"),
                                         'sentence': 'Hello',
                                         'response': "Hi There",
                                         'matched_nodes': [{'type': 'Topic',
                                                            'node': 'ONEORMORE [*]',
                                                            'words': [],
                                                            'multi_word': True,
                                                            'wild_card': True},
                                                           {'type': 'Word',
                                                            'node': 'WORD [Hi]',
                                                            'words': ['Hi'], 'multi_word': False,
                                                            'wild_card': False},
                                                           {'type': 'Word',
                                                            'node': 'WORD [There]',
                                                            'words': ['There'],
                                                            'multi_word': False,
                                                            'wild_card': False}]}}

        sentence = Sentence.from_json(self._client_context, json_data)

        self.assertIsNotNone(sentence)
        self.assertEqual(sentence.words, ['One', 'Two', 'Three'])
        self.assertEqual(sentence.response, "Hello")
        self.assertEqual(sentence.positivity, 0.0)
        self.assertEqual(sentence.subjectivity, 0.5)
        self.assertIsNotNone(sentence.matched_context)
