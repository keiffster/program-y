import unittest
import os
import os.path

from programy.rdf.collection import RDFCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory


class RDFCollectionLoadingTests(unittest.TestCase):

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

    def test_reload_from_file(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.delete_entity("TEST1", "HASPURPOSE", "to test")
        self.assertFalse(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.reload(factory, "TESTDATA")

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

