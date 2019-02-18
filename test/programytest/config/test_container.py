import unittest

from programy.config.container import BaseContainerConfigurationData


class BaseContainerConfigurationDataTests(unittest.TestCase):

    def test_init(self):

        container = BaseContainerConfigurationData("container")
        self.assertEqual(container.section_name, "container")
        with self.assertRaises(NotImplementedError):
            container.load_configuration(None, None)