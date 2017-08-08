
from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateResetLearnNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateResetLearnNode()
        self.assertIsNotNone(root)

