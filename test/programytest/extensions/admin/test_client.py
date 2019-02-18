import unittest.mock

from programy.extensions.admin.client import ClientAdminExtension

from programytest.client import TestClient


class ClientAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ClientAdminExtensionClient, self).load_configuration(arguments)


class ClientAdminExtensionTests(unittest.TestCase):

    def test_client_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()
        self.assertEqual("LIST BOTS, LIST BRAINS, DUMP BRAIN", extension.execute(client_context, "COMMANDS"))

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

    def test_client_dump_brain(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Brain dumped, see config for location", extension.execute(client_context, "DUMP BRAIN bot brain"))

