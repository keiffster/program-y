import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.interval import TemplateIntervalNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateIntervalNode(TemplateIntervalNode):
    def __init__(self):
        TemplateIntervalNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateIntervalNodeTests(ParserTestsBaseClass):

    def test_node_years(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        self.assertEqual("[INTERVAL]", node.to_string())
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("years")
        node.interval_from = TemplateWordNode("Thu Oct 06 16:35:11 2014")
        node.interval_to = TemplateWordNode("Fri Oct 07 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")


    def test_node_months(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("months")
        node.interval_from = TemplateWordNode("Thu Jul  6 16:35:11 2014")
        node.interval_to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "3")

    def test_node_weeks(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("weeks")
        node.interval_from = TemplateWordNode("Thu Oct  1 16:35:11 2016")
        node.interval_to = TemplateWordNode("Fri Oct  14 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_days(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("days")
        node.interval_from = TemplateWordNode("Thu Oct  6 16:35:11 2016")
        node.interval_to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_hours(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("hours")
        node.interval_from = TemplateWordNode("Thu Oct  7 12:35:11 2016")
        node.interval_to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "4")

    def test_node_minutes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("minutes")
        node.interval_from = TemplateWordNode("Thu Oct 7 16:33:09 2016")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_seconds(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("seconds")
        node.interval_from = TemplateWordNode("Thu Oct 7 16:35:09 2016")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_microseconds(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("microseconds")
        node.interval_from = TemplateWordNode("Thu Oct 7 16:35:09 2016")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:09 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "0")

    def test_node_ymd(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("ymd")
        node.interval_from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2 years, 2 months, 23 days")

    def test_node_hms(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("hms")
        node.interval_from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "0 hours, 2 minutes, 2 seconds")

    def test_node_unknown(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("unknown")
        node.interval_from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_node_ymdhms(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("ymdhms")
        node.interval_from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2 years, 2 months, 23 days, 0 hours, 2 minutes, 2 seconds")


    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateIntervalNode()
        node.interval_format = TemplateWordNode("%c")
        node.style = TemplateWordNode("years")
        node.interval_from = TemplateWordNode("Thu Oct 6 16:35:11 2014")
        node.interval_to = TemplateWordNode("Fri Oct 7 16:35:11 2016")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><interval format="%c" style="years"><from>Thu Oct 6 16:35:11 2014</from><to>Fri Oct 7 16:35:11 2016</to></interval></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateIntervalNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)