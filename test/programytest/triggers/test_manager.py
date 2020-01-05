import unittest
from typing import Dict

from programy.context import ClientContext
from programy.triggers.config import TriggerConfiguration
from programy.triggers.manager import TriggerManager


class MockTriggerManager(TriggerManager):

    def __init__(self, config: TriggerConfiguration):
        TriggerManager.__init__(self, config)

    def trigger(self, event: str, client_context: ClientContext = None, additional: Dict[str, str] = None) -> bool:
        return


class TriggerManagerTests(unittest.TestCase):

    def test_init(self):
        mgr = MockTriggerManager(TriggerConfiguration())
        self.assertIsNotNone(mgr)

    def test_init_with_events(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

        self.assertIsInstance(mgr, TriggerManager)

