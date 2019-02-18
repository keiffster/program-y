from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils
import programytest.storage.engines as Engines


class SQLStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)
        self.assertIsNone(engine._session)

    def test_users(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.user_asserts(engine)

    def test_linked_accounts(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.linked_account_asserts(engine)

    def test_links(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.link_asserts(engine)

    def test_properties(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.property_asserts(engine)

    def test_conversations(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(engine)

    def test_categories(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.category_asserts(engine)
