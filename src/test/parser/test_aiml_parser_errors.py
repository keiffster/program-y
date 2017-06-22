import unittest
import os
from xml.etree.ElementTree import ParseError

from programy.parser.aiml_parser import AIMLParser
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.brain import BrainFileConfiguration

class AIMLParserErrorTests(unittest.TestCase):

    def setUp(self):
        config = BrainConfiguration()
        config._aiml_files = BrainFileConfiguration(errors="/tmp/errors.txt")
        test_brain = Brain(configuration=config)
        self.parser = AIMLParser(brain=test_brain)
        self.parser.create_debug_storage(config)
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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, no template node found in category\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, no template node found in category\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Topic name empty or null\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error unknown child node of topic, xxxx\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Topic node text is empty\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Topic node text is empty\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("That node text is empty\n", self.parser._errors[0])

    def test_base_aiml_topic_no_name(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, missing name attribute for topic\n", self.parser._errors[0])

    def test_base_aiml_topic_no_category(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, no categories in topic\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, no template node found in category\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, topic exists in category AND as parent node\n", self.parser._errors[0])

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
        self.assertEquals(1, len(self.parser._errors))
        self.assertEquals("Error, no template node found in category\n", self.parser._errors[0])

