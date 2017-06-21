import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.request import TemplateRequestNode
from programy.dialog import Question, Conversation


from test.parser.template.base import TemplateTestsBaseClass


class TemplateRequestNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        self.bot._conversations["testid"] = conversation

        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        question = Question.create_from_text("What did you say")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><request /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><request index="3" position="2" /></template>', xml_str)
