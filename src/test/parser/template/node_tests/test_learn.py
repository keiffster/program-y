import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import TemplateLearnNode, LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass

class TemplateLearnNodeTests(TemplateTestsBaseClass):

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

        resolved = root.resolve(self.bot, self.clientid)
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

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learn><category><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></category></learn></template>", xml_str)

