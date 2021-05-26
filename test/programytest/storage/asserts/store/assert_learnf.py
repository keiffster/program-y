import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.client import TestClient


class LearnfStoreAsserts(unittest.TestCase):

    def assert_save_learnf(self, store):

        store.empty()

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))

        category = LearnCategory(ET.Element("HELLO"), ET.Element("*"), ET.Element("*"), template)

        store.save_learnf(client_context, category)

