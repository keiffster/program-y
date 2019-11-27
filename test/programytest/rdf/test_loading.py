import os
import os.path
import unittest
from unittest.mock import patch
from programy.rdf.collection import RDFCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


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

        self.assertTrue(collection.load(factory))

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

    def test_load_no_engine(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(factory))

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

        self.assertTrue(collection.load(factory))

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.delete_entity("TEST1", "HASPURPOSE", "to test")
        self.assertFalse(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        self.assertTrue(collection.reload(factory, "TESTDATA"))

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

    def test_reload_no_engine(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.reload(factory, "TESTDATA"))

    def patch_load_all(self, collector):
        raise Exception ("Mock Exception")

    @patch("programy.storage.stores.file.store.rdfs.FileRDFStore.load_all", patch_load_all)
    def test_load_exception(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(factory))


    def patch_reload(self, collector, rdf_name):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.rdfs.FileRDFStore.reload", patch_reload)
    def test_reload_from_file_exception(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(factory))

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.delete_entity("TEST1", "HASPURPOSE", "to test")
        self.assertFalse(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        self.assertFalse(collection.reload(factory, "TESTDATA"))
