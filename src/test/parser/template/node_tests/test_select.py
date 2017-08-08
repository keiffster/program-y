
from programy.parser.template.nodes.select import TemplateSelectNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateSelectNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateSelectNode()
        self.assertIsNotNone(root)

