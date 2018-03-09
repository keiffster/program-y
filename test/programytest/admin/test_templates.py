import unittest

from programy.admin.templates import *

class TemplateTests(unittest.TestCase):

    def test_templates_exist(self):
        self.assertIsNotNone(AIML_TEMPLATE)
        self.assertIsNotNone(LOGGING_TEMPLATE)
        self.assertIsNotNone(CONFIG_TEMPLATE)
        self.assertIsNotNone(REST_CONFIG)
        self.assertIsNotNone(WEBCHAT_CONFIG)
        self.assertIsNotNone(TWITTER_CONFIG)
        self.assertIsNotNone(XMPP_CONFIG)
        self.assertIsNotNone(SOCKET_CONFIG)
        self.assertIsNotNone(INITIAL_PROPERTIES)
        self.assertIsNotNone(CONSOLE_SHELL_SCRIPT)
        self.assertIsNotNone(WEBCHAT_SHELL_SCRIPT)
        self.assertIsNotNone(REST_SHELL_SCRIPT)
        self.assertIsNotNone(XMPP_SHELL_SCRIPT)
        self.assertIsNotNone(TWITTER_SHELL_SCRIPT)
        self.assertIsNotNone(SOCKET_SHELL_SCRIPT)
        self.assertIsNotNone(CONSOLE_WINDOWS_CMD)
        self.assertIsNotNone(WEBCHAT_WINDOWS_CMD)
        self.assertIsNotNone(REST_WINDOWS_CMD)
        self.assertIsNotNone(XMPP_WINDOWS_CMD)
        self.assertIsNotNone(TWITTER_WINDOWS_CMD)
        self.assertIsNotNone(SOCKET_WINDOWS_CMD)
