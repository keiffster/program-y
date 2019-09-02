import unittest
import os

from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.template import PatternTemplateNode

from programy.dialog.sentence import Sentence
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient

class AIMLParserTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AIMLParserTestClient, self).load_storage()
        self.add_default_stores()


class AIMLParserTests(unittest.TestCase):

    def setUp(self):
        self._client = AIMLParserTestClient()
        self._client_context = self._client.create_client_context("testid")
        self.parser = self._client_context.brain.aiml_parser

    def test_tag_name_from_namespace(self):
        tag, namespace = self.parser.tag_and_namespace_from_text("aiml")
        self.assertEqual("aiml", tag)
        self.assertIsNone(namespace)

        tag, namespace = self.parser.tag_and_namespace_from_text("{http://alicebot.org/2001/AIML}aiml")
        self.assertEqual("aiml", tag)
        self.assertEqual("{http://alicebot.org/2001/AIML}", namespace)

    def test_parse_from_file_valid(self):
        filename = os.path.dirname(__file__)+ '/valid.aiml'
        self.parser.parse_from_file(filename)

    def test_aiml_with_namespace(self):
        self.parser.parse_from_text(
        """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01"
                  xmlns="http://alicebot.org/2001/AIML"
                  xmlns:aiml="http://alicebot.org/2001/AIML"
                  xmlns:html="http://www.w3.org/TR/REC-html40">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        template = that.star.template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_topic_category_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </category>
                </topic>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        template = that.star.template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_topic_category_template_multi_line(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                        <template>
                            RESPONSE1,
                            RESPONSE2.
                            RESPONSE3
                        </template>
                    </category>
                </topic>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        template = that.star.template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE1, RESPONSE2. RESPONSE3")

    def test_base_aiml_category_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        template = that.star.template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_category_template_that(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <that>something</that>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertEqual(len(that.children), 1)
        self.assertIsNotNone(that.children[0])
        self.assertIsInstance(that.children[0], PatternWordNode)
        self.assertEqual(that.children[0].word, "something")

        template = that.children[0].template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_category_template_topic(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <topic>something</topic>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "something")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        template = that.star.template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_category_template_topic_that(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <that>something</that>
                    <topic>other</topic>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)

        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertTrue(self.parser.pattern_parser.root.has_one_or_more())

        node = self.parser.pattern_parser.root.star
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)
        self.assertEqual(node.wildcard, "*")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "other")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertEqual(len(that.children), 1)
        self.assertIsNotNone(that.children[0])
        self.assertIsInstance(that.children[0], PatternWordNode)
        self.assertEqual(that.children[0].word, "something")

        template = that.children[0].template
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PatternTemplateNode)
        self.assertEqual(template.template.resolve(self._client_context), "RESPONSE")

    def test_base_aiml_multiple_categories(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>Hello</pattern>
                    <template>Hiya</template>
                </category>
                <category>
                    <pattern>Goodbye</pattern>
                    <template>See ya</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser.pattern_parser)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertIsInstance(self.parser.pattern_parser.root, PatternRootNode)
        self.assertEqual(2, len(self.parser.pattern_parser.root.children))

        node = self.parser.pattern_parser.root.children[1]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "Hello")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        node = self.parser.pattern_parser.root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "Goodbye")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

    def test_base_aiml_multiple_categories_in_a_topic(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>Hello</pattern>
                        <template>Hiya</template>
                    </category>
                    <category>
                        <pattern>Goodbye</pattern>
                        <template>See ya</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertEqual(2, len(self.parser.pattern_parser.root.children))

        node = self.parser.pattern_parser.root.children[1]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "Hello")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        node = self.parser.pattern_parser.root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "Goodbye")

        topic = node.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

    def test_base_aiml_multiple_categories_in_and_out_of_topic(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>Welcome</pattern>
                    <template>Hello there</template>
                </category>
                <topic name="test">
                    <category>
                        <pattern>Hello</pattern>
                        <template>Hiya</template>
                    </category>
                    <category>
                        <pattern>Goodbye</pattern>
                        <template>See ya</template>
                    </category>
                </topic>
                <category>
                    <pattern>Interesting</pattern>
                    <template>Yes</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser.pattern_parser.root)
        self.assertEqual(4, len(self.parser.pattern_parser.root.children))

        node1 = self.parser.pattern_parser.root.children[0]
        self.assertIsNotNone(node1)
        self.assertIsInstance(node1, PatternWordNode)
        self.assertEqual(node1.word, "Interesting")

        topic = node1.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        node2 = self.parser.pattern_parser.root.children[1]
        self.assertIsNotNone(node2)
        self.assertIsInstance(node2, PatternWordNode)
        self.assertEqual(node2.word, "Goodbye")

        topic = node2.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        node3 = self.parser.pattern_parser.root.children[2]
        self.assertIsNotNone(node3)
        self.assertIsInstance(node3, PatternWordNode)
        self.assertEqual(node3.word, "Hello")

        topic = node3.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertEqual(len(topic.children), 1)
        self.assertIsNotNone(topic.children[0])
        self.assertIsInstance(topic.children[0], PatternWordNode)
        self.assertEqual(topic.children[0].word, "test")

        that = topic.children[0].that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

        node4 = self.parser.pattern_parser.root.children[3]
        self.assertIsNotNone(node4)
        self.assertIsInstance(node4, PatternWordNode)
        self.assertEqual(node4.word, "Welcome")

        topic = node4.topic
        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, PatternTopicNode)
        self.assertTrue(topic.has_one_or_more())
        self.assertIsInstance(topic.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic.star.wildcard, "*")

        that = topic.star.that
        self.assertIsNotNone(that)
        self.assertIsInstance(that, PatternThatNode)
        self.assertTrue(that.has_one_or_more())
        self.assertIsInstance(that.star, PatternOneOrMoreWildCardNode)
        self.assertEqual(that.star.wildcard, "*")

    def test_match_sentence(self):

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>HELLO</pattern>
                    <template>Hiya</template>
                </category>
            </aiml>
            """)

        self.parser.pattern_parser.dump()

        context = self.parser.match_sentence(self._client_context, Sentence(self._client_context, "HELLO"), "*", "*")
        self.assertIsNotNone(context)
        self.assertEqual("Hiya", context.template_node.template.resolve(self._client_context))

    def test_inline_br_html(self):

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>HELLO</pattern>
                    <template>Hello  <br/> World</template>
                </category>
            </aiml>
            """)

    def test_inline_bold_html(self):

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>HELLO</pattern>
                    <template>Hello <bold>You</bold> World</template>
                </category>
            </aiml>
            """)

    def test_iset(self):

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>Hello</pattern>
                    <template>Hi There</template>
                </category>
                <category>
                    <pattern># <iset>who, what</iset> are you</pattern>
                    <template>OK thanks</template>
                </category>
                <category>
                    <pattern># <iset>who, what</iset> is he</pattern>
                    <template>OK thanks</template>
                </category>
            </aiml>
            """)

    def test_duplicate_topics(self):

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="TOPIC1">
                    <category>
                        <pattern>*</pattern>
                        <template>
                            Test Text
                        </template>
                    </category>
                </topic>
                <topic name="TOPIC2">
                    <category>
                        <pattern>*</pattern>
                        <template>
                            Test Text
                        </template>
                    </category>
                </topic>
            </aiml>
            """)
