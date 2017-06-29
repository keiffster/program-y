from programy.parser.template.nodes.atttrib import TemplateAttribNode

from test.parser.template.base import TemplateTestsBaseClass

######################################################################################################################
#
class TemplateAttribTests(TemplateTestsBaseClass):

    def test_node(self):
        attrib = TemplateAttribNode()
        self.assertIsNotNone(attrib)
        with self.assertRaises(Exception):
            attrib.set_attrib("Something", "Other")
