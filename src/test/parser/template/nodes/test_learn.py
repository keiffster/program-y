import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import TemplateLearnNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


#TODO These tests are meaningless, the node is not tested for a learnf syntac

class TemplateLearnNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnNode()
        self.assertIsNotNone(learn)
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")

        root.append(learn)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnNode()
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")
        root.append(learn)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learn><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></learn></template>", xml_str)

