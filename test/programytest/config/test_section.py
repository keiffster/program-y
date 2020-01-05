import unittest

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class MockBaseSectionConfigurationData(BaseSectionConfigurationData):

    def __init__(self, name):
        BaseSectionConfigurationData.__init__(self, name)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        raise NotImplementedError()


class BaseSectionConfigurationDataTests(unittest.TestCase):

    def test_init(self):

        section = MockBaseSectionConfigurationData("section")
        self.assertEqual(section.section_name, "section")
        with self.assertRaises(NotImplementedError):
            section.load_config_section(None, None, None)