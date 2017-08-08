
from programy.parser.template.nodes.uniq import TemplateUniqNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateUniqNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)

