import unittest

from programy.security.linked import LinkedAccountsManager


class MockStorageEngine(object):
    pass


class LinkedAccountsManagerTests(unittest.TestCase):

    def test_init(self):
        storage_engine = MockStorageEngine()

        mgr = LinkedAccountsManager(storage_engine)
        self.assertIsNotNone(mgr)

    def test_generate_key(self):
        storage_engine = MockStorageEngine()

        mgr = LinkedAccountsManager(storage_engine)

        key = mgr._generate_key()
        self.assertIsNotNone(key)
        self.assertEqual(8, len(key))

        key = mgr._generate_key(size=12)
        self.assertIsNotNone(key)
        self.assertEqual(12, len(key))


"""
Workflow is 

1. User is associated with an initial PRIMARY Client, e.g Facebook

2. User decides to link account and ask PY to initiate an action

3. PY asks them to login into primary account and ask for a LINK TOKEN
    As part of the process they are asked to provide a SECRET they know
    PY then provides a LINK TOKEN
    User now has
                PRIMARY ACCOUNT ID
                PRIMARY ACCOUNT NAME
                GIVEN TOKEN
                GENERATED TOKEN
                
    Link has a expirary time, circa 1 hr, after which link expires and now tokens will need to be requested
                
4. PY now tells them to log into the client they want to link

5. User logs into secondary account and asks to link this to primary account

6. PY Asks for 
                PRIMARY ACCOUNT ID
                PRIMARY ACCOUNT NAME
                GIVEN TOKEN
                GENERATED TOKEN

7. PY Links accounts

"""