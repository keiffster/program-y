import unittest

from programy.security.manager import SecurityManager
from programy.config.brain.securities import BrainSecuritiesConfiguration


class TestSecurityManager(unittest.TestCase):

    def test_init(self):
        config = BrainSecuritiesConfiguration()
        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)



