import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.word import PatternWordNode
from programytest.client import TestClient


class ConversationTests(unittest.TestCase):

    def test_pop_methods(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        conversation.record_dialog(question1)
        self.assertEquals(1, len(conversation.questions))

        question2 = Question.create_from_text(client_context, "How are you")
        conversation.record_dialog(question2)
        self.assertEquals(2, len(conversation.questions))

        conversation.pop_dialog()
        self.assertEquals(1, len(conversation.questions))

        conversation.pop_dialog()
        self.assertEquals(0, len(conversation.questions))

        conversation.pop_dialog()
        self.assertEquals(0, len(conversation.questions))

    def test_properties(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)

        conversation.set_property("name1", "value1")
        self.assertEquals("value1", conversation.property("name1"))
        conversation.set_property("name2", "value2")
        self.assertEquals("value2", conversation.property("name2"))
        conversation.set_property("name2", "value3")
        self.assertEquals("value3", conversation.property("name2"))
        self.assertEquals(None, conversation.property("name3"))

    def test_topic_pattern(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)

        self.assertEquals("*", conversation.get_topic_pattern(client_context))

        conversation.set_property("topic", "TOPIC1")

        self.assertEquals("TOPIC1", conversation.get_topic_pattern(client_context))

    def test_topic_pattern_topic_none(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        conversation.set_property("topic", None)

        self.assertEquals("*", conversation.get_topic_pattern(client_context))

        conversation.set_property("topic", "TOPIC1")

        self.assertEquals("TOPIC1", conversation.get_topic_pattern(client_context))


    def test_parse_last_sentences_from_response(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)

        self.assertEquals("*", conversation.parse_last_sentences_from_response(""))
        self.assertEquals("*", conversation.parse_last_sentences_from_response("."))
        self.assertEquals("HELLO", conversation.parse_last_sentences_from_response("HELLO"))
        self.assertEquals("HELLO THERE", conversation.parse_last_sentences_from_response("HELLO THERE"))
        self.assertEquals("THERE", conversation.parse_last_sentences_from_response("HELLO. THERE"))
        self.assertEquals("THERE", conversation.parse_last_sentences_from_response("HELLO. THERE!"))

    def test_that_pattern(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)

        self.assertEquals("*", conversation.parse_last_sentences_from_response(""))
        self.assertEquals("HELLO", conversation.parse_last_sentences_from_response("HELLO"))
        self.assertEquals("HELLO", conversation.parse_last_sentences_from_response(".HELLO"))
        self.assertEquals("HELLO", conversation.parse_last_sentences_from_response("HELLO."))
        self.assertEquals("HELLO", conversation.parse_last_sentences_from_response(".HELLO."))
        self.assertEquals("HELLO THERE", conversation.parse_last_sentences_from_response("HELLO THERE"))
        self.assertEquals("THERE", conversation.parse_last_sentences_from_response("HELLO. THERE"))
        self.assertEquals("THERE", conversation.parse_last_sentences_from_response("HELLO. THERE!"))

    def test_conversation(self):

        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual(0, len(conversation._questions))
        self.assertEqual(3, conversation._max_histories)
        self.assertEqual(1, len(conversation._properties))

        with self.assertRaises(Exception):
            conversation.current_question()
        with self.assertRaises(Exception):
            conversation.previous_nth_question(0)

        question1 = Question.create_from_text(client_context, "Hello There")
        conversation.record_dialog(question1)
        self.assertEqual(question1, conversation.current_question())
        with self.assertRaises(Exception):
            conversation.previous_nth_question(1)

        question2 = Question.create_from_text(client_context, "Hello There Again")
        conversation.record_dialog(question2)
        self.assertEqual(question2, conversation.current_question())
        self.assertEqual(question1, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(3)

        question3 = Question.create_from_text(client_context, "Hello There Again Again")
        conversation.record_dialog(question3)
        self.assertEqual(question3, conversation.current_question())
        self.assertEqual(question2, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(4)

        # Max Histories for this test is 3
        # Therefore we should see the first question, pop of the stack

        question4 = Question.create_from_text(client_context, "Hello There Again Again Again")
        conversation.record_dialog(question4)
        self.assertEqual(question4, conversation.current_question())
        self.assertEqual(question3, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(5)

    def test_parse_last_sentences_from_response(self):

        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        self.assertIsNotNone(conversation)

        response = "Hello World"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Hello World", that)

        response = "Hello World. Second sentence"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Second sentence", that)

        response = "Hello World. Second sentence. Third Sentence"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Third Sentence", that)

    def test_to_json(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation1 = Conversation(client_context)
        conversation1.properties["convo1"] = "value1"
        matched_context = MatchContext(100, 100)
        matched_context.matched_nodes.append(Match(Match.WORD, PatternWordNode("Hello"), "Hello"))
        sentence = Sentence(client_context, text="Hi", response="Hello there", matched_context=matched_context)

        question1 = Question.create_from_sentence(sentence)
        question1.properties['quest1'] = "value2"
        conversation1.record_dialog(question1)

        json_data = conversation1.to_json()
        self.assertIsNotNone(json_data)

        self.assertEqual("testclient", json_data['client_context']['clientid'])
        self.assertEqual("testid", json_data['client_context']['userid'])
        self.assertEqual("bot", json_data['client_context']['botid'])
        self.assertEqual("brain", json_data['client_context']['brainid'])
        self.assertEqual(0, json_data['client_context']['depth'])

        conversation2 = Conversation.from_json(client_context, json_data)

        self.assertEqual(conversation1._client_context.client.id, conversation2._client_context.client.id)
        self.assertEqual(conversation1._client_context.userid, conversation2._client_context.userid)
        self.assertEqual(conversation1._client_context.bot.id, conversation2._client_context.bot.id)
        self.assertEqual(conversation1._client_context.brain.id, conversation2._client_context.brain.id)
        self.assertEqual(conversation1._client_context._question_start_time,
                          conversation2._client_context._question_start_time)
        self.assertEqual(conversation1._client_context._question_depth, conversation2._client_context._question_depth)
        self.assertEqual(conversation1._client_context._id, conversation2._client_context._id)

        self.assertEqual(conversation1.properties, conversation2.properties)
        self.assertEqual(conversation1.max_histories, conversation2.max_histories)

        self.assertNotEquals(0, len(conversation1.questions))
        self.assertNotEquals(0, len(conversation2.questions))
        self.assertEqual(len(conversation1.questions), len(conversation2.questions))

        for i in range(len(conversation2.questions)):
            q1 = conversation1.questions[i]
            q2 = conversation2.questions[i]

            self.assertEqual(q1.srai, q2.srai)
            self.assertEqual(q1._current_sentence_no, q2._current_sentence_no)

            self.assertEqual(q1.properties, q2.properties)

            self.assertNotEquals(0, len(q1.sentences))
            self.assertNotEquals(0, len(q2.sentences))
            self.assertEqual(len(q1.sentences), len(q2.sentences))

            for j in range(len(q2.sentences)):
                s1 = q1.sentences[j]
                s2 = q2.sentences[j]

                self.assertEqual(s1.words, s2.words)
                self.assertEqual(s1.response, s2.response)
                self.assertEqual(s1.positivity, s2.positivity)
                self.assertEqual(s1.subjectivity, s2.subjectivity)

                mc1 = s1.matched_context
                mc2 = s2.matched_context

                self.assertEquals(mc1.template_node, mc2.template_node)
                self.assertEquals(mc1.max_search_depth, mc2.max_search_depth)
                self.assertEquals(mc1.max_search_timeout, mc2.max_search_timeout)
                time1 = mc1._total_search_start.strftime("%d/%m/%Y, %H:%M:%S")
                time2 = mc2._total_search_start.strftime("%d/%m/%Y, %H:%M:%S")
                self.assertEquals(time1, time2)

                self.assertNotEquals(0, len(mc1.matched_nodes))
                self.assertNotEquals(0, len(mc2.matched_nodes))
                self.assertEquals(len(mc1.matched_nodes), len(mc2.matched_nodes))

                for k in range(len(mc1.matched_nodes)):
                    mn1 = mc1.matched_nodes[k]
                    mn2 = mc2.matched_nodes[k]

                    self.assertEquals(mn1._matched_node_str, mn2._matched_node_str)
                    self.assertEquals(mn1._matched_node_type, mn2._matched_node_type)
                    self.assertEquals(mn1._matched_node_multi_word, mn2._matched_node_multi_word)
                    self.assertEquals(mn1._matched_node_wildcard, mn2._matched_node_wildcard)
                    self.assertEquals(mn1._matched_node_words, mn2._matched_node_words)

