import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphListProcessingTests(unittest.TestCase):

    def setUp(self):
        self.parser = TemplateGraph()
        self.assertIsNotNone(self.parser)

        self.test_brain = None
        test_config = ClientConfiguration()
        self.test_bot = Bot(Brain(BrainConfiguration()), config=test_config.bot_configuration)
        self.test_clientid = "testid"


    def test_first(self):
        template = ET.fromstring("""
            <template>
                <first>one two three four</first>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "one")

    def test_rest(self):
        template = ET.fromstring("""
            <template>
                <rest>one two three four</rest>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "two three four")

if __name__ == '__main__':
    unittest.main()
