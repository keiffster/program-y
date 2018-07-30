import unittest
import os.path
import xml.etree.ElementTree as ET

from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programytest.client import TestClient


class FileLearnfStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_save_learnf(self):
        config = FileStorageConfiguration()
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

        xml_node =  ET.fromstring("""
            <category>
                <pattern>HELLO</pattern>
                <template>Hi there</template>
            </category>
        """)

        store.save_learnf(client_context, xml_node)

        self.assertTrue(os.path.exists(learnf_fullpath))
