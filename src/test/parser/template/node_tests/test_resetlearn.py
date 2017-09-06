from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode
from programy.parser.template.nodes.base import TemplateNode

from test.parser.template.base import TemplateTestsBaseClass

class MockTemplateResetLearnNode(TemplateResetLearnNode):
    def __init__(self):
        TemplateResetLearnNode.__init__(self)

    def resolve_to_string(self, bot, clientid):
        raise Exception("This is an error")

class TemplateResetLearnNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateResetLearnNode()
        self.assertIsNotNone(root)
        self.assertEquals("", root.resolve(self.bot, self.clientid))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateResetLearnNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)

    def test_to_string(self):
        node = MockTemplateResetLearnNode()
        self.assertEquals("RESETLEARN", node.to_string())

    def test_to_xml(self):
        node = TemplateResetLearnNode()
        self.assertEquals("<resetlearn />", node.to_xml(self.bot, self.clientid))