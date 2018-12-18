import unittest
import os
import shutil

from programy.admin.tool import AdminTool


class MockAdminTool(AdminTool):
    pass


class AdminToolTests(unittest.TestCase):

    text = ""

    @staticmethod
    def display(text):
        AdminToolTests.text += text

    def setUp(self):
        AdminToolTests.text = ""

    def test_invalid_commands(self):
        tool = AdminTool()
        tool.run([], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Invalid command []"))

    def test_unknown_primary_command(self):
        tool = AdminTool()
        tool.run(['unknown'], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Unknown primary command [unknown]"))

    def test_missing_bot_name(self):
        tool = AdminTool()
        tool.run(['download'], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Missing bot name from download command"))

    def test_list_bots(self):
        tool = AdminTool()
        tool.run([], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Invalid command []"))
