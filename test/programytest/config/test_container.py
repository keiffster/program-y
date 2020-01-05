import unittest

from programy.config.container import BaseContainerConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class MockBaseContainerConfigurationData(BaseContainerConfigurationData):

    def __init__(self, name):
        BaseContainerConfigurationData.__init__(self, name)

    def load_configuration(self, configuration_file, bot_root, subs: Substitutions = None):
        raise NotImplementedError()


class BaseContainerConfigurationDataTests(unittest.TestCase):

    def test_init(self):
        container = MockBaseContainerConfigurationData("container")
        self.assertEqual(container.section_name, "container")
        with self.assertRaises(NotImplementedError):
            container.load_configuration(None, None)
