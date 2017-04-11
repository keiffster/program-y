import xml.etree.ElementTree as ET

from programy.parser.template.nodes.condchild import TemplateConditionNodeWithChildren
from programy.parser.template.nodes.condlistitem import TemplateConditionListItemNode

from test.parser.template.base import TemplateTestsBaseClass


class TestTemplateConditionNodeWithChildren(TemplateTestsBaseClass):

    def test_get_default(self):
        node = TemplateConditionNodeWithChildren()
        self.assertIsNotNone(node)

        node.append(TemplateConditionListItemNode("cond1", "value1"))
        node.append(TemplateConditionListItemNode("cond2", "value2"))
        node.append(TemplateConditionListItemNode("cond3"))

        self.assertEqual(3, len(node.children))

        default = node.get_default()
        self.assertIsNotNone(default)
        self.assertEqual(default.name, "cond3")
