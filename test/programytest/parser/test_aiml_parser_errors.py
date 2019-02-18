import unittest
import os
from xml.etree.ElementTree import ParseError

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient
from programy.utils.classes.loader import ClassLoader

class AIMLParserErrorTests(unittest.TestCase):

    def setUp(self):
        bot_config = BotConfiguration()

        bot = Bot(bot_config, TestClient())

        bot.brain.configuration.debugfiles._save_errors = True
        bot.brain.configuration.debugfiles._save_duplicates = True

        bot.brain.template_factory.add_node("base", ClassLoader.instantiate_class("programy.parser.template.nodes.base.TemplateNode") )
        bot.brain.template_factory.add_node("word", ClassLoader.instantiate_class("programy.parser.template.nodes.word.TemplateWordNode") )
        bot.brain.pattern_factory.add_node("oneormore", ClassLoader.instantiate_class("programy.parser.pattern.nodes.oneormore.PatternOneOrMoreWildCardNode") )

        bot.brain.pattern_factory.add_node("topic", ClassLoader.instantiate_class("programy.parser.pattern.nodes.topic.PatternTopicNode") )
        bot.brain.pattern_factory.add_node("that", ClassLoader.instantiate_class("programy.parser.pattern.nodes.that.PatternThatNode") )
        bot.brain.pattern_factory.add_node("template", ClassLoader.instantiate_class("programy.parser.pattern.nodes.template.PatternTemplateNode") )

        self.parser = bot.brain.aiml_parser

        self.parser.create_debug_storage()
        self.assertIsNotNone(self.parser)

    def test_parse_from_file_invalid(self):
        filename = os.path.dirname(__file__)+ '/invalid.aiml'
        self.parser.parse_from_file(filename)

    def test_no_content(self):
        with self.assertRaises(ParseError) as raised:
            self.parser.parse_from_text(
                """
                """)

    def test_crud(self):
        with self.assertRaises(ParseError) as raised:
            self.parser.parse_from_text(
                """Blah Blah Blah
                """)

    def test_no_aiml(self):
        with self.assertRaises(ParseError) as raised:
            self.parser.parse_from_text(
                """<?xml version="1.0" encoding="UTF-8"?>
                """)
        self.assertTrue(str(raised.exception).startswith("no element found:"))

    def test_base_aiml_category_no_content(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual('No template node found in category', self.parser._errors[0][0])

    def test_base_aiml_category_no_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][0])

    def test_base_aiml_topic_empty_parent_node(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="">
                    <category>
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic name empty or null", self.parser._errors[0][0])

    def test_base_aiml_topic_with_something_else(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <xxxx>
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </xxxx>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Unknown child node of topic, xxxx", self.parser._errors[0][0])

    def test_base_aiml_topic_empty_child_node1(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <topic name="" />
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic node text is empty", self.parser._errors[0][0])

    def test_base_aiml_topic_empty_child_node2(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <topic></topic>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic node text is empty", self.parser._errors[0][0])

    def test_base_aiml_that_empty_child_node(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <that></that>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("That node text is empty", self.parser._errors[0][0])

    def test_base_aiml_topic_no_name(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Missing name attribute for topic", self.parser._errors[0][0])

    def test_base_aiml_topic_no_category(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No categories in topic", self.parser._errors[0][0])

    def test_base_aiml_topic_category_no_content(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][0])

    def test_base_aiml_topic_at_multiple_levels(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <topic name="test2" />
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic exists in category AND as parent node", self.parser._errors[0][0])

    def test_base_aiml_topic_category_no_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][0])
