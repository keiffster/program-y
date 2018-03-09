import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.vocabulary import TemplateVocabularyNode
from programy.bot import Bot, BotConfiguration
from programy.brain import Brain, BrainConfiguration
from programy.mappings.sets import SetLoader

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateVocabularyNode(TemplateVocabularyNode):
    def __init__(self):
        TemplateVocabularyNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateVocabularyNodeTests(ParserTestsBaseClass):

    def test_node(self):

        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        pattern_element = ET.fromstring("<pattern>hello world</pattern>")
        self._client_context.brain._aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, None)

        loader = SetLoader()

        self._client_context.brain.sets.add_set("testset", loader.load_from_text("""
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

        self.assertEquals(root.resolve(self._client_context), '5')

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateVocabularyNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><vocabulary>Test</vocabulary></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateVocabularyNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals("", result)