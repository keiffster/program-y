import xml.etree.ElementTree as ET
import unittest

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import TemplateLearnNode, LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateLearnNode(TemplateLearnNode):
    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TestLearnCategory(unittest.TestCase):

    def test_init(self):
        learncat = LearnCategory("pattern", "topic", "that", "template")
        self.assertIsNotNone(learncat)
        self.assertIsNotNone(learncat._pattern)
        self.assertIsNotNone(learncat._topic)
        self.assertIsNotNone(learncat._that)
        self.assertIsNotNone(learncat._template)
        self.assertIsNotNone(learncat.children)
        self.assertEqual(0, len(learncat.children))

        self.assertEqual("[CATEGORY]", learncat.to_string())

        learncat.pattern = "pattern2"
        self.assertEqual("pattern2", learncat.pattern)
        learncat.topic = "topic2"
        self.assertEqual("topic2", learncat.topic)
        learncat.that = "that2"
        self.assertEqual("that2", learncat.that)
        learncat.template = "template2"
        self.assertEqual("template2", learncat.template)

        learncat.append("category1")
        learncat.append("category2")
        self.assertEqual(2, len(learncat.children))


class TemplateLearnNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnNode()
        self.assertIsNotNone(learn)

        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)

        root.append(learn)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnNode()
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learn><category><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></category></learn></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLearnNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)