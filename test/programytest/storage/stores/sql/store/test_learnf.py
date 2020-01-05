import unittest

import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.learnf import SQLLearnfStore
from programytest.storage.asserts.store.assert_learnf import LearnfStoreAsserts
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.client import TestClient


class SQLLearnfStoreTests(LearnfStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLearnfStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_save_learnf(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLearnfStore(engine)

        self.assert_save_learnf(store)

    def test_get_all(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLearnfStore(engine)

        with self.assertRaises(Exception):
            store._get_all()
