import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.carousel import TemplateCarouselNode
from programy.parser.template.nodes.richmedia.card import TemplateCardNode
from programy.parser.template.nodes.richmedia.button import TemplateButtonNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateCarouselNodeTests(ParserTestsBaseClass):

    def test_carousel_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        carousel = TemplateCarouselNode()

        card = TemplateCardNode()
        card._image = TemplateWordNode("http://Servusai.com")
        card._title = TemplateWordNode("Servusai.com")
        card._subtitle = TemplateWordNode("The home of ProgramY")

        button = TemplateButtonNode()
        button._text = TemplateWordNode("More...")
        button._url = TemplateWordNode("http://Servusai.com/aiml")
        card._buttons.append(button)

        carousel._cards.append(card)

        root.append(carousel)

        resolved = root.resolve(self._client_context)

        self.assertIsNotNone(resolved)
        self.assertEqual("<carousel><card><image>http://Servusai.com</image><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle><button><text>More...</text><url>http://Servusai.com/aiml</url></button></card></carousel>", resolved)

        self.assertEqual("<carousel><card><image>http://Servusai.com</image><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle><button><text>More...</text><url>http://Servusai.com/aiml</url></button></card></carousel>", root.to_xml(self._client_context))

