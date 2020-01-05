import os
import unittest
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order
from programy.parser.aiml_parser import AIMLParser
from programy.dialog.sentence import Sentence
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programytest.client import TestClient
from programy.parser.exceptions import ParserException
from programy.parser.exceptions import DuplicateGrammarException


class MockElement(ET.Element):

    def __init__(self, tag, attrib={}):
        ET.Element.__init__(self, tag, attrib)
        self._start_line_number = 0
        self._end_line_number = 0


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

    def test__getstate__(self):
        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_template_parser'])
        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_num_categories'])
        self.assertIsNone(self.parser.__getstate__().get('_brain', None))
        self.assertIsNone(self.parser.__getstate__().get('_errors', None))
        self.assertIsNone(self.parser.__getstate__().get('_duplicates', None))

    def test__getstate__with_errors_and_duplicates(self):
        self.parser._errors = []
        self.parser._duplicates = []
        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_template_parser'])
        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_num_categories'])
        self.assertIsNone(self.parser.__getstate__().get('_brain', None))
        self.assertIsNone(self.parser.__getstate__().get('_errors', None))
        self.assertIsNone(self.parser.__getstate__().get('_duplicates', None))

    def test__getstate__without_errors_and_duplicates(self):

        if '_errors' in self.parser.__dict__:
            del self.parser.__dict__['_errors']
        if '_duplicates' in self.parser.__dict__:
            del self.parser.__dict__['_duplicates']

        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_template_parser'])
        self.assertIsNotNone(self.parser.__getstate__()['_aiml_loader'])
        self.assertIsNotNone(self.parser.__getstate__()['_num_categories'])
        self.assertIsNone(self.parser.__getstate__().get('_brain', None))
        self.assertIsNone(self.parser.__getstate__().get('_errors', None))
        self.assertIsNone(self.parser.__getstate__().get('_duplicates', None))

    def test_check_aiml_tag(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
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

        tag_name, namespace = AIMLParser.check_aiml_tag(aiml)
        self.assertEquals("aiml", tag_name)
        self.assertEquals("{http://alicebot.org/2001/AIML}", namespace)

    def test_check_aiml_tag_no_aiml(self):
        aiml = None
        with self.assertRaises(ParserException):
            tag_name, namespace = AIMLParser.check_aiml_tag(aiml)

    def test_check_aiml_tag_no_namespace(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        tag_name, namespace = AIMLParser.check_aiml_tag(aiml)
        self.assertEquals("aiml", tag_name)
        self.assertEquals(None, namespace)

    def test_check_aiml_tag_not_aiml(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aipl version="1.01"
                  xmlns="http://alicebot.org/2001/AIML"
                  xmlns:aiml="http://alicebot.org/2001/AIML"
                  xmlns:html="http://www.w3.org/TR/REC-html40">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aipl>
        """)

        with self.assertRaises(ParserException):
            _, _ = AIMLParser.check_aiml_tag(aiml)

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

    def test_duplicate_categories_in_topic(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._duplicates))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="Topic1">
                    <category>
                        <pattern>HELLO</pattern>
                        <template>Hi There</template>
                    </category>
                    <category>
                        <pattern>HELLO</pattern>
                        <template>Hi There</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._duplicates))

    def test_duplicate_topic(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <topic name="TOPIC1" />
                    <pattern>*</pattern>
                    <template>
                        Test Text
                    </template>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_duplicate_that(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <that name="THAT1" />
                    <that name="THAT1" />
                    <pattern>*</pattern>
                    <template>
                        Test Text
                    </template>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_duplicate_pattern(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <that name="THAT1" />
                    <pattern>*</pattern>
                    <pattern>*</pattern>
                    <template>
                        Test Text
                    </template>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_no_pattern(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <that name="THAT1" />
                    <template>
                        Test Text
                    </template>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_duplicate_template(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <that name="THAT1" />
                    <pattern>*</pattern>
                    <template>
                        Test Text
                    </template>
                    <template>
                        Test Text
                    </template>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_no_template(self):
        self.parser._errors = []
        self.parser._duplicates = []

        self.assertEquals(0, len(self.parser._errors))
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
               <category>
                    <topic name="TOPIC1" />
                    <that name="THAT1" />
                    <pattern>*</pattern>
                </category>
            </aiml>
            """)
        self.assertEquals(1, len(self.parser._errors))

    def test_no_topic_no_category(self):
        with self.assertRaises(ParserException):
            self.parser.parse_from_text(
                """<?xml version="1.0" encoding="UTF-8"?>
                <aiml>
                   <categoryX>
                        <topic name="TOPIC1" />
                        <that name="THAT1" />
                        <pattern>*</pattern>
                        <template>
                            Test Text
                        </template>
                    </categoryX>
                </aiml>
                """)

    def get_temp_dir(self):
        if os.name == 'posix':
            return '/tmp'
        elif os.name == 'nt':
            import tempfile
            return tempfile.gettempdir()
        else:
            raise Exception("Unknown operating system [%s]" % os.name)

    def test_save_debug_files(self):
        tmpdir = self.get_temp_dir()
        errors_file = tmpdir + os.sep + "debug/errors.txt"
        duplicates_file = tmpdir + os.sep + "debug/duplicates.txt"

        self._client.add_debug_stores(errors_file, duplicates_file)

        if os.path.exists(errors_file):
            os.remove(errors_file)

        if os.path.exists(duplicates_file):
            os.remove(duplicates_file)

        self.parser.brain.configuration.debugfiles._save_errors = True
        self.parser.brain.configuration.debugfiles._save_duplicates = True

        self.parser._errors = []
        self.parser._errors.append(["test error message", "test.aiml1", 100, 106])
        self.parser._duplicates = []
        self.parser._duplicates.append(["test duplicate message", "test.aiml2", 200, 206])

        self.parser.save_debug_files()

        self.assertTrue(os.path.exists(errors_file))
        self.assertTrue(os.path.exists(duplicates_file))

        if os.path.exists(errors_file):
            os.remove(errors_file)

        if os.path.exists(duplicates_file):
            os.remove(duplicates_file)

        self.parser.display_debug_info()

    def test_save_debug_files_no_storage(self):
        tmpdir = self.get_temp_dir()
        errors_file = tmpdir + os.sep + "debug/errors.txt"
        duplicates_file = tmpdir + os.sep + "debug/duplicates.txt"

        if os.path.exists(errors_file):
            os.remove(errors_file)

        if os.path.exists(duplicates_file):
            os.remove(duplicates_file)

        self.parser.brain.configuration.debugfiles._save_errors = True
        self.parser.brain.configuration.debugfiles._save_duplicates = True

        self.parser._errors = []
        self.parser._errors.append(["test error message", "test.aiml1", 100, 106])
        self.parser._duplicates = []
        self.parser._duplicates.append(["test duplicate message", "test.aiml2", 200, 206])

        self.parser.save_debug_files()

        self.assertFalse(os.path.exists(errors_file))
        self.assertFalse(os.path.exists(duplicates_file))

    def test_handle_aiml_duplicate_no_expression(self):
        self.parser._duplicates = []
        duplicate = DuplicateGrammarException("test duplicate message")
        self.parser.handle_aiml_duplicate(duplicate, "test.aiml", None)

        self.assertEquals([['test duplicate message', 'test.aiml', None, None]], self.parser._duplicates)

    def test_handle_aiml_error_no_expression(self):
        self.parser._errors = []
        duplicate = DuplicateGrammarException("test duplicate message")
        self.parser.handle_aiml_error(duplicate, "test.aiml", None)

        self.assertEquals([['test duplicate message', 'test.aiml', None, None]], self.parser._errors)

    def test_handle_aiml_duplicate_no_duplicates(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        duplicate = DuplicateGrammarException("test duplicate message")
        self.parser.handle_aiml_duplicate(duplicate, "test.aiml", aiml)

        self.assertEquals(None, self.parser._duplicates)

    def test_handle_aiml_error_no_errors(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        error = ParserException("test parser exception")
        self.parser.handle_aiml_error(error, "test.aiml", aiml)

        self.assertEquals(None, self.parser._errors)

    def test_handle_aiml_duplicate_without_line_numbers(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        self.parser._duplicates = []
        duplicate = DuplicateGrammarException("test duplicate message")
        self.parser.handle_aiml_duplicate(duplicate, "test.aiml", aiml)

        self.assertEquals([['test duplicate message', 'test.aiml', None, None]], self.parser._duplicates)

    def test_handle_aiml_error_without_line_numbers(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <aiml version="1.01">
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
        """)

        error = ParserException("test parser exception")
        self.parser.handle_aiml_error(error, "test.aiml", aiml)

        self.assertEquals([['test parser exception', 'test.aiml', '0', '0']], self.parser._errors)

    def test_handle_aiml_duplicate_with_line_numbers(self):
        aiml = MockElement("aiml")
        aiml._start_line_number = 99
        aiml._end_line_number = 999
        self.parser._duplicates = []
        duplicate = DuplicateGrammarException("test duplicate message")
        self.parser.handle_aiml_duplicate(duplicate, "test.aiml", aiml)

        self.assertEquals([['test duplicate message', 'test.aiml', '99', '999']], self.parser._duplicates)

    def test_handle_aiml_error_without_line_numbers(self):
        aiml = MockElement("aiml")
        aiml._start_line_number = 99
        aiml._end_line_number = 999
        self.parser._errors = []
        error = ParserException("test parser exception")
        self.parser.handle_aiml_error(error, "test.aiml", aiml)

        self.assertEquals([['test parser exception', 'test.aiml', '99', '999']], self.parser._errors)

