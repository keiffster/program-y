import unittest.mock
from unittest.mock import patch
from programy.extensions.admin.client import ClientAdminExtension
from programytest.client import TestClient


class ClientAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ClientAdminExtensionClient, self).load_configuration(arguments)


class ClientAdminExtensionTests(unittest.TestCase):

    def test_invalid_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Invalid Admin Command, LIST or DUMP only", extension.execute(client_context, "XXXXX"))

    def test_command_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()
        self.assertEqual("LIST BOTS, LIST BRAINS, DUMP BRAIN", extension.execute(client_context, "COMMANDS"))

    def test_invalid_list_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Invalid LIST command, BOTS or BRAINS only", extension.execute(client_context, "LIST"))
        self.assertEqual("Invalid LIST command, BOTS or BRAINS only", extension.execute(client_context, "LIST XXXXX"))
        self.assertEqual("Invalid LIST command, BOTS or BRAINS only", extension.execute(client_context, "LIST BRAINS"))

    def test_client_list_bots(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("bot", extension.execute(client_context, "LIST BOTS"))

    def test_client_list_brains(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("brain", extension.execute(client_context, "LIST BRAINS bot"))

    def test_client_list_brains_bot_unkown(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Invalid Bot Id [botX]", extension.execute(client_context, "LIST BRAINS botX"))

    def test_invalid_dump_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Invalid DUMP command, BRAIN only", extension.execute(client_context, "DUMP XXXXX"))
        self.assertEqual("Incomplete DUMP BRAIN Command", extension.execute(client_context, "DUMP BRAIN"))
        self.assertEqual("Invalid Bot Id [BOTX]", extension.execute(client_context, "DUMP BRAIN BOTX BRAINY"))
        self.assertEqual("Invalid Brain Id [BRAINY]", extension.execute(client_context, "DUMP BRAIN bot BRAINY"))
        self.assertEqual("Incomplete DUMP BRAIN Command", extension.execute(client_context, "DUMP BRAIN bot"))

    def test_client_dump_brain(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Brain dumped, see config for location", extension.execute(client_context, "DUMP BRAIN bot brain"))

    def patch_commands(self):
        raise Exception("Mock Exception")

    @patch("programy.extensions.admin.client.ClientAdminExtension._commands", patch_commands)
    def test_client_exception(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Client Admin Error", extension.execute(client_context, "COMMANDS"))
