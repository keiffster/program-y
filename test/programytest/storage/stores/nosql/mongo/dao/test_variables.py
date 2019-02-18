import unittest

from programy.storage.stores.nosql.mongo.dao.variable import Variables


class VariablesTests(unittest.TestCase):

    def test_init_no_id(self):
        variables = Variables(clientid='client1', userid='user1', variables={'var1': 'val1', 'val2': 'val2'})

        self.assertIsNotNone(variables)
        self.assertIsNone(variables.id)
        self.assertEqual('client1', variables.clientid)
        self.assertEqual('user1', variables.userid)
        self.assertEqual({'var1': 'val1', 'val2': 'val2'}, variables.variables)
        self.assertEqual({'clientid': 'client1', 'userid': 'user1', 'variables': {'val2': 'val2', 'var1': 'val1'}}, variables.to_document())

    def test_init_with_id(self):
        variables = Variables(clientid='client1', userid='user1', variables={'var1': 'val1', 'val2': 'val2'})
        variables.id = '666'

        self.assertIsNotNone(variables)
        self.assertIsNotNone(variables.id)
        self.assertEqual('666', variables.id)
        self.assertEqual('client1', variables.clientid)
        self.assertEqual('user1', variables.userid)
        self.assertEqual({'var1': 'val1', 'val2': 'val2'}, variables.variables)
        self.assertEqual({'_id': '666', 'clientid': 'client1', 'userid': 'user1', 'variables': {'val2': 'val2', 'var1': 'val1'}}, variables.to_document())

    def test_from_document(self):
        variables1 = Variables.from_document({'clientid': 'client1', 'userid': 'user1', 'variables': {'val2': 'val2', 'var1': 'val1'}})
        self.assertIsNotNone(variables1)
        self.assertIsNone(variables1.id)
        self.assertEqual('client1', variables1.clientid)
        self.assertEqual('user1', variables1.userid)
        self.assertEqual({'var1': 'val1', 'val2': 'val2'}, variables1.variables)

        variables2 = Variables.from_document({'_id': '666', 'clientid': 'client1', 'userid': 'user1', 'variables': {'val2': 'val2', 'var1': 'val1'}})
        self.assertIsNotNone(variables2)
        self.assertIsNotNone(variables2.id)
        self.assertEqual('666', variables2.id)
        self.assertEqual('client1', variables2.clientid)
        self.assertEqual('user1', variables2.userid)
        self.assertEqual({'var1': 'val1', 'val2': 'val2'}, variables2.variables)
