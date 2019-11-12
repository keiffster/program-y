from programy.parser.exceptions import ParserException
from programy.parser.template.graph import TemplateGraph
from programytest.parser.base import ParserTestsBaseClass


class TemplateGraphTests(ParserTestsBaseClass):

    def test_init(self):
        graph = TemplateGraph(self._client_context.brain.aiml_parser)
        self.assertIsNotNone(graph)
        self.assertEquals(self._client_context.brain.aiml_parser, graph.aiml_parser)
        self.assertEquals(self._client_context.brain.template_factory, graph.template_factory)

    def test_get_node_class_by_name(self):
        graph = TemplateGraph(self._client_context.brain.aiml_parser)

        node = graph.get_node_class_by_name("base")
        self.assertIsNotNone(node)

    def test_get_node_class_by_name_missing(self):
        graph = TemplateGraph(self._client_context.brain.aiml_parser)

        with self.assertRaises(ParserException):
            _ = graph.get_node_class_by_name("other")
