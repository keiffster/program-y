
from programy.parser.template.nodes.tuple import TemplateTupleNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateTupleNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateTupleNode()
        self.assertIsNotNone(root)

