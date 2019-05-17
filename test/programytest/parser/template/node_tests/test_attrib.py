from programy.parser.template.nodes.attrib import TemplateAttribNode

from programytest.parser.base import ParserTestsBaseClass


class TemplateAttribNodeTests(ParserTestsBaseClass):

    def test_node(self):
        attrib = TemplateAttribNode()
        self.assertIsNotNone(attrib)
        with self.assertRaises(Exception):
            attrib.set_attrib("Something", "Other")
