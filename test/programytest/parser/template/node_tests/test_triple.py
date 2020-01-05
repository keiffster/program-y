from programy.parser.template.nodes.triple import TemplateTripleNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateTripleNodeTests(ParserTestsBaseClass):

    def test_children_to_xml_all_there(self):
        node = TemplateTripleNode("triple", subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        self.assertEqual("<subj>S</subj><pred>P</pred><obj>O</obj>", node.children_to_xml(self._client_context))

    def test_children_to_xml_no_subj(self):
        node = TemplateTripleNode("triple", pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        self.assertEqual("<pred>P</pred><obj>O</obj>", node.children_to_xml(self._client_context))

    def test_children_to_xml_no_pred(self):
        node = TemplateTripleNode("triple", subj=TemplateWordNode("S"), obj=TemplateWordNode("O"))
        self.assertEqual("<subj>S</subj><obj>O</obj>", node.children_to_xml(self._client_context))

    def test_children_to_xml_no_obj(self):
        node = TemplateTripleNode("triple", subj=TemplateWordNode("S"), pred=TemplateWordNode("P"))
        self.assertEqual("<subj>S</subj><pred>P</pred>", node.children_to_xml(self._client_context))
