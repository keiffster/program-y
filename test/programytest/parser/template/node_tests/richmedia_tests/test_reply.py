import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.reply import TemplateReplyNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateReplyNodeTests(ParserTestsBaseClass):

    def test_text_reply_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        reply = TemplateReplyNode()
        reply._text = TemplateWordNode("SAY HELLO")

        root.append(reply)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<reply><text>SAY HELLO</text></reply>", resolved)

        self.assertEqual("<reply><text>SAY HELLO</text></reply>", root.to_xml(self._client_context))

    def test_text_postback__replynode(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        reply = TemplateReplyNode()
        reply._text = TemplateWordNode("SAY HELLO")
        reply._postback = TemplateWordNode("HELLO")

        root.append(reply)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<reply><text>SAY HELLO</text><postback>HELLO</postback></reply>", resolved)

        self.assertEqual("<reply><text>SAY HELLO</text><postback>HELLO</postback></reply>", root.to_xml(self._client_context))
