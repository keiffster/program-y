import unittest

from programytest.client import TestClient

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

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS LIST")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>MONKEY</li></ul>", result)

    def test_subjects_count(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS COUNT")
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

    def test_predicates(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "PREDICATES MONKEY")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>LEGS</li></ul>", result)

    def test_objects(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMAL")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "OBJECT MONKEY LEGS")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>2</li></ul>", result)
