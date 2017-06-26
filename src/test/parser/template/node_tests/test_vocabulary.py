import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.vocabulary import TemplateVocabularyNode
from programy.bot import Bot, BotConfiguration
from programy.brain import Brain, BrainConfiguration
from programy.mappings.sets import SetLoader

from test.parser.template.base import TemplateTestsBaseClass


class TemplateVocabularyNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        pattern_element = ET.fromstring("<pattern>hello world</pattern>")
        test_bot.brain._aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, None)

        loader = SetLoader()

        test_bot.brain.sets.add_set("testset", loader.load_from_text("""
        val1
        val2
        val3
        """))

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateVocabularyNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEquals(root.resolve(test_bot, "testid"), '5')

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateVocabularyNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><vocabulary>Test</vocabulary></template>", xml_str)

