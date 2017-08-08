
from programy.parser.template.nodes.resetlearnf import TemplateResetLearnfNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateResetLearnfNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateResetLearnfNode()
        self.assertIsNotNone(root)

