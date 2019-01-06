import unittest
import os.path
import xml.etree.ElementTree as ET
import shutil

from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.client import TestClient


class FileLearnfStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)
        self.assertEqual(store.storage_engine, engine)

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

        store.save_learnf(client_context, category)

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
