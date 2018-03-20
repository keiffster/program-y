import unittest

from programytest.aiml_tests.client import TestClient

from programy.extensions.admin.rdf import RDFAdminExtension


class RDFAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(RDFAdminExtensionClient, self).load_configuration(arguments)


class RDFAdminExtensionTests(unittest.TestCase):

    def test_subjects_list(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS LIST")
        self.assertIsNotNone(result)
        self.assertEquals("<ul><li>MONKEY</li></ul>", result)

    def test_subjects_count(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS COUNT")
        self.assertIsNotNone(result)
        self.assertEquals("1", result)

    def test_predicates(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "PREDICATES MONKEY")
        self.assertIsNotNone(result)
        self.assertEquals("<ul><li>LEGS</li></ul>", result)

    def test_objects(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "OBJECT MONKEY LEGS")
        self.assertIsNotNone(result)
        self.assertEquals("<ul><li>2</li></ul>", result)
