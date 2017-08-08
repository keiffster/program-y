
from programy.parser.template.nodes.addtriple import TemplateAddTripleNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateAddTripleNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateAddTripleNode()
        self.assertIsNotNone(root)

