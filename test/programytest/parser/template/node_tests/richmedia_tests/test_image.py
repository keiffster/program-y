import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.image import TemplateImageNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateImageNodeTests(ParserTestsBaseClass):

    def test_image_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        image = TemplateImageNode()

        url = TemplateWordNode("http://Servusai.com/logo.png")

        root.append(image)
        image.append(url)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<image>http://Servusai.com/logo.png</image>", resolved)

        self.assertEqual("<image>http://Servusai.com/logo.png</image>", root.to_xml(self._client_context))

