import unittest

from programy.admin.tool import AdminTool


class MockAdminTool(AdminTool):

    def __init__(self):
        AdminTool.__init__(self)
        self.text = ""

    def display(self, text):
        self.text += text


class AdminToolTests(unittest.TestCase):

    def test_unknown_primary_command(self):
        tool = MockAdminTool()
        tool.run(['unknown'])
        self.assertIsNotNone(tool.text)
        self.assertTrue(tool.text.startswith("Unknown primary command [unknown]"))

    def test_missing_bot_name(self):
        tool = MockAdminTool()
        tool.run(['download'])
        self.assertIsNotNone(tool.text)
        self.assertTrue(tool.text.startswith("Missing bot name from download command"))
