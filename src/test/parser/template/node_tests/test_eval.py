import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateEvalNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        eval = TemplateEvalNode()
        root.append(eval)

        eval.append(TemplateWordNode("hello"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("hello", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateEvalNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><eval>Test</eval></template>", xml_str)

