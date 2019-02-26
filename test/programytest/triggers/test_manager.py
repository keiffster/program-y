import unittest
import os

from programy.triggers.manager import TriggerManager
from programy.triggers.config import TriggerConfiguration


class TriggerManagerTests(unittest.TestCase):

    def test_init(self):

        mgr = TriggerManager(TriggerConfiguration())
        self.assertIsNotNone(mgr)

    def test_init_with_events(self):

        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

        self.assertIsInstance(mgr, TriggerManager)

