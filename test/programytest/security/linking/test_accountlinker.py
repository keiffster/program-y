import unittest

from programy.security.linking.accountlinker import BasicAccountLinkerService


class MockUser(object):
    pass

class MockUserStore(object):

    def __init__(self):
        self.users = {}

    def add_user(self, userid, clientid):
        if userid not in self.users:
            self.users[userid] = []
        if clientid not in self.users[userid]:
            self.users[userid].append(clientid)
        return MockUser()

    def exists(self, userid, clientid):
        if userid in self.users:
            links = self.users[userid]
            return clientid in links
        return False

    def get_links(self, userid):
        if userid in self.users:
            return self.users[userid]
        return []

    def remove_user(self, userid, clientid):
        if userid in self.users:
            if clientid in self.users[userid]:
                self.users[userid].remove(clientid)
            if len(self.users[userid]) == 0:
                del self.users[userid]
            return True
        return False

class MockLink(object):

    def __init__(self, data):
        self.userid = data['userid']
        self.generated_key = data['generated_key']
        self.provided_key = data['provided_key']
        self.expired = data['expired']
        self.expires = data['expires']
        self.retry_count = data['retry_count']

class MockLinkStore(object):

    def __init__(self):
        self.links = {}

    def create_link(self, userid, generated_key, provided_key, expires):

        self.links[userid] = {'userid': userid, 'generated_key': generated_key, 'provided_key': provided_key, 'expired': False, 'expires': expires, 'retry_count': 0}
        return MockLink(self.links[userid])

    def get_link(self, userid):
        if userid in self.links:
            return MockLink(self.links[userid])
        return None

    def link_exists(self, userid, provided_key, generated_key):
        if userid in self.links:
            link = self.links[userid]
            if link['generated_key'] == generated_key and link['provided_key'] == provided_key:
                return True
        return False

    def update_link(self, link):
        self.links[link.userid] =  {'userid': link.userid,
                                    'generated_key': link.generated_key,
                                    'provided_key': link.provided_key,
                                    'expired': link.expired,
                                    'expires': link.expires,
                                    'retry_count': link.retry_count}

    def remove_link(self, userid):
        if userid in self.links.keys():
            del self.links[userid]
            return True
        return False

class MockAccountLink(object):
    pass

class MockLinkedAccount(object):

    def __init__(self):
        self.links = {}
        self.lookup = {}

    def link_accounts(self, primary_userid, linked_userid):
        if primary_userid not in self.links:
            self.links[primary_userid] = []
        if linked_userid not in self.links[primary_userid]:
            self.links[primary_userid].append(self.links[primary_userid])
            self.lookup[linked_userid] = primary_userid
        return MockAccountLink()

    def primary_account(self, secondary_userid):
        if secondary_userid in self.lookup:
            return self.lookup[secondary_userid]
        return None

    def unlink_accounts(self, userid):
        del self.links[userid]
        toremove = []
        for key, value in self.lookup.items():
            if value == userid:
                toremove.append(key)
        for key in toremove:
            del self.lookup[key]
        return True

class MockStorageEngine(object):

    def __init__(self):
        self.user_store = MockUserStore()
        self.link_store = MockLinkStore()
        self.linked_account_store = MockLinkedAccount()


class BasicAccountLinkerServiceTests(unittest.TestCase):

    def test_init(self):
        storage_engine = MockStorageEngine()

        mgr = BasicAccountLinkerService(storage_engine)
        self.assertIsNotNone(mgr)

    def test_generate_key(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        key = mgr._generate_key()
        self.assertIsNotNone(key)
        self.assertEqual(8, len(key))

        key = mgr._generate_key(size=12)
        self.assertIsNotNone(key)
        self.assertEqual(12, len(key))

    def test_generate_expirary(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        expires = mgr._generate_expirary(lifetime=1)
        self.assertIsNotNone(expires)

    def test_happy_path(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, given_key, generated_key, "testuser2", "facebook")
        self.assertTrue(result)

        primary = mgr.primary_account("testuser2")
        self.assertTrue(primary)
        self.assertEquals(primary_user, primary)

    def test_user_client_link_already_exists(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = mgr.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEquals(1, len(links))
        self.assertEquals(primary_client, links[0])

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = mgr.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEquals(1, len(links))
        self.assertEquals(primary_client, links[0])

    def test_given_key_not_matched(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, "PASSWORD2", generated_key, secondary_user, secondary_client)
        self.assertFalse(result)

    def test_generated_key_not_matched(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, given_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

    def test_generated_key_expired(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key, lifetime=0)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, given_key, generated_key, "testuser2", "facebook")
        self.assertFalse(result)

    def test_lockout_after_max_retries(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, given_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = mgr.link_accounts(primary_user, given_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = mgr.link_accounts(primary_user, given_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = mgr.link_accounts(primary_user, given_key, generated_key, secondary_user, secondary_client)
        self.assertFalse(result)

        reset = mgr.reset_link(primary_user)
        self.assertTrue(reset)

        result = mgr.link_accounts(primary_user, given_key, generated_key, secondary_user, secondary_client)
        self.assertTrue(result)

    def test_unlink_user_from_client(self):
        storage_engine = MockStorageEngine()
        mgr = BasicAccountLinkerService(storage_engine)

        primary_user = "testuser1"
        primary_client = "console"
        given_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, given_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, given_key, generated_key, secondary_user, secondary_client)
        self.assertTrue(result)

        result = mgr.unlink_user_from_client(primary_user, primary_client)
        self.assertTrue(result)

        result = mgr.link_accounts(primary_user, given_key, generated_key, secondary_user, secondary_client)
        self.assertFalse(result)
