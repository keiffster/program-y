import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.uniq import TemplateUniqNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateUniqNode(TemplateUniqNode):
    def __init__(self):
        TemplateUniqNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateUniqNodeTests(ParserTestsBaseClass):

    def add_data(self, collection):
        collection.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

    def test_match_only_vars(self):
        self.add_data(self._client_context.brain.rdf)

        node = TemplateUniqNode(subj=TemplateWordNode("MONKEY"), pred=TemplateWordNode("LEGS"), obj=TemplateWordNode("?legs"))
        result = TemplateUniqNode._match_only_vars(self._client_context, "MONKEY", "LEGS", "?z")
        self.assertIsNotNone(result)
        self.assertEquals([[['?z', '2']]], result)

    def test_match_only_vars_no_brain(self):
        self._client_context.brain = None

        node = TemplateUniqNode(subj=TemplateWordNode("MONKEY"), pred=TemplateWordNode("LEGS"), obj=TemplateWordNode("?legs"))
        result = TemplateUniqNode._match_only_vars(self._client_context, "MONKEY", "LEGS", "?z")
        self.assertIsNotNone(result)
        self.assertEquals([], result)

    def test_match_only_vars_no_rdf(self):
        self._client_context.brain._rdf_collection = None

        node = TemplateUniqNode(subj=TemplateWordNode("MONKEY"), pred=TemplateWordNode("LEGS"), obj=TemplateWordNode("?legs"))
        result = TemplateUniqNode._match_only_vars(self._client_context, "MONKEY", "LEGS", "?z")
        self.assertIsNotNone(result)
        self.assertEquals([], result)

    def test_filter_results(self):
        self.add_data(self._client_context.brain.rdf)

        node = TemplateUniqNode(subj=TemplateWordNode("MONKEY"), pred=TemplateWordNode("LEGS"), obj=TemplateWordNode("2"))

        self.assertEquals([], TemplateUniqNode._filter_results([]))
        self.assertEquals([2], TemplateUniqNode._filter_results([ [ [1, 2] ] ]))
        self.assertEquals([2, 3], TemplateUniqNode._filter_results([ [ [1, 2], [1, 3] ] ]))
        self.assertEquals([2], TemplateUniqNode._filter_results([ [ [1, 2], [2, 2] ] ]))

    def test_to_string(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)
        self.assertEqual("[UNIQ]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uniq><subj>S</subj><pred>P</pred><obj>O</obj></uniq></template>", xml_str)

    def test_node_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode()

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_no_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateUniqNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

