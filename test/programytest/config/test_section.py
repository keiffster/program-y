import unittest

from programy.config.section import BaseSectionConfigurationData


class BaseSectionConfigurationDataTests(unittest.TestCase):

    def test_init(self):

        section = BaseSectionConfigurationData("section")
        self.assertEqual(section.section_name, "section")
        with self.assertRaises(NotImplementedError):
            section.load_config_section(None, None, None)