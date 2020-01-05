from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.button import TemplateButtonNode
from programy.parser.template.nodes.richmedia.card import TemplateCardNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateCardNodeTests(ParserTestsBaseClass):

    def test_card_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        card = TemplateCardNode()
        card._image = TemplateWordNode("http://Servusai.com")
        card._title = TemplateWordNode("Servusai.com")
        card._subtitle = TemplateWordNode("The home of ProgramY")

        button = TemplateButtonNode()
        button._text = TemplateWordNode("More...")
        button._url = TemplateWordNode("http://Servusai.com/aiml")
        card._buttons.append(button)

        root.append(card)

        resolved = root.resolve(self._client_context)

        self.assertIsNotNone(resolved)
        self.assertEqual("<card><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle><image>http://Servusai.com</image><button><text>More...</text><url>http://Servusai.com/aiml</url></button></card>", resolved)

        self.assertEqual("<card><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle><image>http://Servusai.com</image><button><text>More...</text><url>http://Servusai.com/aiml</url></button></card>", root.to_xml(self._client_context))

    def test_to_xml_no_subtitle_or_image(self):
        card = TemplateCardNode()
        card._title = TemplateWordNode("Servusai.com")

        self.assertEquals("<card><title>Servusai.com</title></card>", card.to_xml(self._client_context))