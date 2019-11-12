import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.triple import TemplateTripleNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphAddTripleTests(TemplateGraphTestClient):

    def test_triple(self):
        template = ET.fromstring("""
			    <triple>
			        <subj>X</subj>
			        <pred>Y</pred>
			        <obj>Z</obj>
			    </triple>
			""")

        triple = TemplateTripleNode("triple")
        triple.parse_expression(self._graph, template)

    def test_triple_attribs(self):
        template = ET.fromstring("""
                <triple subj="X" pred="Y" obj="Z" >
                </triple>
            """)

        triple = TemplateTripleNode("triple")
        triple.parse_expression(self._graph, template)

    def test_triple(self):
        template = ET.fromstring("""
			    <triple>
			        <subj>X</subj>
			        <pred>Y</pred>
			        <obj>Z</obj>
			        <id/>
			    </triple>
			""")

        triple = TemplateTripleNode("triple")
        with self.assertRaises(ParserException):
            triple.parse_expression(self._graph, template)
