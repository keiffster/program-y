import unittest
import os
from programy.storage.entities.category import CategoryReadOnlyStore
from programy.storage.entities.category import CategoryReadWriteStore
from programy.storage.entities.store import Store
import xml.etree.ElementTree as ET
from programytest.client import TestClient
from programy.dialog.sentence import Sentence


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

