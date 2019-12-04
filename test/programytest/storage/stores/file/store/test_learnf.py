import os.path
import shutil
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.config import FileStoreConfiguration
from programytest.client import TestClient


class FileLearnfStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        self.assertEquals('/tmp/categories/learnf', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_storage_path_multi_paths(self):
        config = FileStorageConfiguration()
        tmpdir = FileStorageConfiguration.get_temp_dir()
        config._learnf_storage = FileStoreConfiguration(dirs=[tmpdir + os.sep + "categories/learnf", tmpdir + os.sep + "categories/learnf2"], extension="aiml",
                                                      subdirs=False, fileformat="xml", encoding="utf-8",
                                                      delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        self.assertEquals('/tmp/categories/learnf', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_save_learnf(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))

        category = LearnCategory(pattern, topic, that, template)

        self.assertTrue(store.save_learnf(client_context, category))

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    @staticmethod
    def patch_write_xml_to_learnf_file(learnf_path):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.learnf.FileLearnfStore._write_xml_to_learnf_file", patch_write_xml_to_learnf_file)
    def test_create_learnf_file_if_missing(self):
        self.assertFalse(FileLearnfStore.create_learnf_file_if_missing("test.xml"))

    def patch_parse(source, parser=None):
        raise Exception("Mock Exception")

    @patch ("xml.etree.ElementTree.parse", patch_parse)
    def test_write_node_to_learnf_file(self):
        config = FileStorageConfiguration()
        tmpdir = FileStorageConfiguration.get_temp_dir() + os.sep + "learnf"
        tmpfile = tmpdir + os.sep + "tmp" + os.sep + "test.xml"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learn_cat = LearnCategory(ET.Element("HELLO"), ET.Element("*"), ET.Element("*"), TemplateWordNode("Hi"))

        node = store.create_category_xml_node(client_context, learn_cat)

        with self.assertRaises(Exception):
            store.write_node_to_learnf_file(client_context, node, tmpfile)

    def test_write_node_to_learnf_file_already_exists(self):
        config = FileStorageConfiguration()
        tmpdir = FileStorageConfiguration.get_temp_dir() + os.sep + "learnf"
        tmpfile = tmpdir + os.sep + "tmp" + os.sep + "test.xml"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learn_cat = LearnCategory(ET.Element("HELLO"), ET.Element("*"), ET.Element("*"), TemplateWordNode("Hi"))

        node = store.create_category_xml_node(client_context, learn_cat)

        store.write_node_to_learnf_file(client_context, node, tmpfile)

        self.assertTrue(os.path.exists(tmpfile))

        store.write_node_to_learnf_file(client_context, node, tmpfile)

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def patch_write_learnf_to_file(self, client_context, category):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.learnf.FileLearnfStore._write_learnf_to_file", patch_write_learnf_to_file)
    def test_save_learnf_with_exception(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))

        category = LearnCategory(pattern, topic, that, template)

        self.assertFalse(store.save_learnf(client_context, category))

    def test_node_already_exists_no_pattern(self):
        root = ET.fromstring("<xml><category><pattern>HELLO</pattern><template>Hi</template></category>"
                             "<category><pattern>YO</pattern><template>Hi</template></category></xml>")
        node = ET.fromstring("<category></category>")

        self.assertFalse(FileLearnfStore.node_already_exists(root, node))

    def test_node_already_exists_root_no_pattern(self):
        root = ET.fromstring("<xml><category></category></xml>")
        node = ET.fromstring("<category><pattern>HELLO</pattern><template>Hi</template></category>")

        self.assertFalse(FileLearnfStore.node_already_exists(root, node))


    def test_node_already_exists_with_pattern(self):
        root = ET.fromstring("<xml><category><pattern>HELLO</pattern><template>Hi</template></category>"
                             "<category><pattern>YO</pattern><template>Hi</template></category></xml>")
        node = ET.fromstring("<category><pattern>HELLO</pattern><template>Hi</template></category>")

        self.assertTrue(FileLearnfStore.node_already_exists(root, node))

    def test_node_already_exists_with_diff_pattern(self):
        root = ET.fromstring("<xml><category><pattern>HEY</pattern><template>Hi</template></category>"
                             "<category><pattern>YO</pattern><template>Hi</template></category></xml>")
        node = ET.fromstring("<category><pattern>HELLO</pattern><template>Hi</template></category>")

        self.assertFalse(FileLearnfStore.node_already_exists(root, node))
