import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.video import TemplateVideoNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateVideoNodeTests(ParserTestsBaseClass):

    def test_video_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        video = TemplateVideoNode()

        url = TemplateWordNode("http://Servusai.com/logo.mov")

        root.append(video)
        video.append(url)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<video>http://Servusai.com/logo.mov</video>", resolved)

        self.assertEqual("<video>http://Servusai.com/logo.mov</video>", root.to_xml(self._client_context))

