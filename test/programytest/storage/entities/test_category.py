import unittest
from unittest.mock import patch
import os
from programy.storage.entities.category import CategoryReadOnlyStore
from programy.storage.entities.category import CategoryReadWriteStore
from programy.storage.entities.store import Store
import xml.etree.ElementTree as ET
from programytest.client import TestClient
from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException


class CategoryStoreTests(unittest.TestCase):

    def test_extract_content(self):
        xml = ET.fromstring("<text>test</text>")
        result = CategoryReadOnlyStore.extract_content("text", xml)
        self.assertEquals("test", result)

    def test_extract_not_found(self):
        xml = ET.fromstring("<text>test</text>")
        result = CategoryReadOnlyStore.extract_content("other", xml)
        self.assertEquals(None, result)

    def test_find_all_no_namespace(self):
        aiml = ET.fromstring( """
            <topic>
                    <category>
                        <pattern>HI</pattern>
                        <template>RESPONSE</template>
                    </category>
                    <category>
                        <pattern>HELLO</pattern>
                        <template>RESPONSE</template>
                    </category>
            </topic>
        """)

        store = CategoryReadOnlyStore()
        found = store.find_all(aiml, "category")
        self.assertIsNotNone(found)
        self.assertEqual(2, len(found))

    def test_find_all_with_namespace(self):
        aiml = ET.fromstring( """<?xml version="1.0" encoding="ISO-8859-1"?>
            <a:aiml version="1.01"
                  xmlns="http://alicebot.org/2001/AIML"
                  xmlns:a="http://alicebot.org/2001/AIML"
                  xmlns:html="http://www.w3.org/TR/REC-html40">
                  <a:topic>
                    <a:category>
                        <a:pattern>HI</a:pattern>
                        <a:template>RESPONSE</a:template>
                    </a:category>
                    <a:category>
                        <a:pattern>HELLO</a:pattern>
                        <a:template>RESPONSE</a:template>
                    </a:category>
                  </a:topic>
            </a:aiml>
        """)

        store = CategoryReadOnlyStore()
        found = store.find_all(aiml, "topic", {"a": "http://alicebot.org/2001/AIML"})
        self.assertIsNotNone(found)
        self.assertEqual(1, len(found))

    def test_find_element_str(self):
        aiml = ET.fromstring( """
            <category>
                <pattern>HI</pattern>
            </category>
        """)

        store = CategoryReadOnlyStore()
        found = store.find_element_str("pattern", aiml)
        self.assertEqual("HI", found)

    def test_find_element_str_not_present(self):
        aiml = ET.fromstring( """
            <category>
                <pattern>HI</pattern>
            </category>
        """)

        store = CategoryReadOnlyStore()
        found = store.find_element_str("topic", aiml)
        self.assertEqual("*", found)

    def test_find_element_str_multi_elements(self):
        aiml = ET.fromstring( """
            <category>
                <pattern>HI</pattern>
                <pattern>HI</pattern>
            </category>
        """)

        store = CategoryReadOnlyStore()
        with self.assertRaises(Exception):
            _ = store.find_element_str("pattern", aiml)


class CategoryTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(CategoryTestClient, self).load_storage()
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()



class CategoryReadOnlyStoreTests(unittest.TestCase):

    def test_load_category(self):
        client = CategoryTestClient()
        client_context = client.create_client_context("test1")
        parser = client_context.brain.aiml_parser

        store = CategoryReadOnlyStore()
        store._load_category("group1", "HELLO", "*", "*", "Test Hello!", parser)

        match = parser.match_sentence(client_context, Sentence(client_context, "HELLO"), "*", "*")
        self.assertIsNotNone(match)

    def test_load_category_duplicate_grammar(self):
        client = CategoryTestClient()
        client_context = client.create_client_context("test1")
        parser = client_context.brain.aiml_parser
        parser.brain.configuration.debugfiles._save_errors = True
        parser.brain.configuration.debugfiles._save_duplicates = True
        parser.create_debug_storage()

        store = CategoryReadOnlyStore()
        self.assertEqual(0, len(parser._duplicates))
        store._load_category("group1", "HELLO", "*", "*", "Test Hello!", parser)
        store._load_category("group1", "HELLO", "*", "*", "Test Hello!", parser)
        self.assertEqual(1, len(parser._duplicates))

        match = parser.match_sentence(client_context, Sentence(client_context, "HELLO"), "*", "*")
        self.assertIsNotNone(match)

    def patch_parse_category1(self, category_xml, namespace, topic_element=None, add_to_graph=True, userid="*"):
        raise ParserException("Mock Exception")

    @patch("programy.parser.aiml_parser.AIMLParser.parse_category", patch_parse_category1)
    def test_load_category_parser_exception(self):
        client = CategoryTestClient()
        client_context = client.create_client_context("test1")
        parser = client_context.brain.aiml_parser
        parser.brain.configuration.debugfiles._save_errors = True
        parser.brain.configuration.debugfiles._save_duplicates = True
        parser.create_debug_storage()

        store = CategoryReadOnlyStore()
        self.assertEqual(0, len(parser._duplicates))
        store._load_category("group1", "HELLO", "*", "*", "Test Hello!", parser)

        match = parser.match_sentence(client_context, Sentence(client_context, "HELLO"), "*", "*")
        self.assertIsNone(match)

    def patch_parse_category2(self, category_xml, namespace, topic_element=None, add_to_graph=True, userid="*"):
        raise Exception("Mock Exception")

    @patch("programy.parser.aiml_parser.AIMLParser.parse_category", patch_parse_category2)
    def test_load_category_parser_exception2(self):
        client = CategoryTestClient()
        client_context = client.create_client_context("test1")
        parser = client_context.brain.aiml_parser
        parser.brain.configuration.debugfiles._save_errors = True
        parser.brain.configuration.debugfiles._save_duplicates = True
        parser.create_debug_storage()

        store = CategoryReadOnlyStore()
        self.assertEqual(0, len(parser._duplicates))
        store._load_category("group1", "HELLO", "*", "*", "Test Hello!", parser)

        match = parser.match_sentence(client_context, Sentence(client_context, "HELLO"), "*", "*")
        self.assertIsNone(match)


class MockCategoryReadWriteStore(CategoryReadWriteStore):

    def __init__(self):
        CategoryReadWriteStore.__init__(self)

    def store_category(self, groupid, userid, topic, that, pattern, template):
        return True


class CategoryReadWriteStoreTests(unittest.TestCase):

    def test_store_category(self):
        category_store = CategoryReadWriteStore()
        with self.assertRaises(NotImplementedError):
            category_store.store_category("groupid", "userid", "topic", "that", "pattern", "template")

    def test_upload_from_file_categories_only(self):
        store = MockCategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "fife.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(3, count)
        self.assertEquals(3, success)

    def test_upload_from_file_with_topic(self):
        store = MockCategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "fifewithtopics.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(3, count)
        self.assertEquals(3, success)

    def test_upload_from_file_with_other(self):
        store = MockCategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "other.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(1, count)
        self.assertEquals(0, success)

    def patch_store_category(self, groupid, userid, topic, that, pattern, template):
        return False

    @patch ("programy.storage.entities.category.CategoryReadWriteStore.store_category", patch_store_category)
    def test_upload_from_file_categories_only(self):
        store = CategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "fife.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(3, count)
        self.assertEquals(0, success)

    @patch ("programy.storage.entities.category.CategoryReadWriteStore.store_category", patch_store_category)
    def test_upload_from_file_with_topic_store_fails(self):
        store = CategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "fifewithtopics.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(3, count)
        self.assertEquals(0, success)

    def patch_upload(self, filename):
        raise Exception("Mock Exception")

    @patch ("programy.storage.entities.category.CategoryReadWriteStore._upload", patch_upload)
    def test_upload_from_file_with_exception(self):
        store = CategoryReadWriteStore()
        filename = os.path.dirname(__file__) + os.sep + "categories" + os.sep + "fife.aiml"
        count, success = store.upload_from_file(filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False)
        self.assertEquals(0, count)
        self.assertEquals(0, success)
