import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.rand import TemplateRandomNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class TemplateNodeMixedTests(ParserTestsBaseClass):

    def test_multirandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        root.append(random1)
        root.append(random2)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1 Test3",
                                    "Test1 Test4",
                                    "Test2 Test3",
                                    "Test2 Test4"])

    def test_nestedrandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        random3 = TemplateRandomNode()
        random3.append(random1)
        random3.append(random1)
        random3.append(random2)

        root.append(random3)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1",
                                    "Test2",
                                    "Test3",
                                    "Test4"])

    def test_mixednodes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        random1.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random1.children), 3)

        root.append(TemplateWordNode("Hello"))
        root.append(random1)
        root.append(TemplateWordNode("World!"))

        self.assertEqual(len(root.children), 3)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Hello Test1 World!", "Hello Test2 World!", "Hello Test3 World!"])


