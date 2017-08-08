from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateDeleteTripleNodeTests(TemplateTestsBaseClass):
    def test_node(self):
        root = TemplateDeleteTripleNode()
        self.assertIsNotNone(root)

