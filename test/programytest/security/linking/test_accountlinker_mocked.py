import unittest

from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.security.linking.accounlinker_asserts import AccountLinkerAsserts


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

    def remove_user_from_all_clients(self, userid):
        if userid in self.users:
            del self.users[userid]


class MockLink(object):

    def __init__(self,  userid, provided_key, generated_key, expires, expired, retry_count ):
        self.userid = userid
        self.provided_key = provided_key
        self.generated_key = generated_key
        self.expires = expires
        self.expired = expired
        self.retry_count = retry_count


class MockLinkStore(object):

    def __init__(self):
        self.links = {}

    def create_link(self, userid, provided_key, generated_key, expires):
        link = MockLink(userid, provided_key, generated_key, expires, False, 0)
        self.links[userid] = link
        return link

    def get_link(self, userid):
        if userid in self.links:
            return self.links[userid]
        return None

    def link_exists(self, userid, provided_key, generated_key):
        if userid in self.links:
            link = self.links[userid]
            if link.generated_key == generated_key and link.provided_key == provided_key:
                return True
        return False

    def update_link(self, link):
        if link.userid in self.links:
            self.links[link.userid].userid = link.userid
            self.links[link.userid].generated_key = link.generated_key
            self.links[link.userid].provided_key = link.provided_key
            self.links[link.userid].expired = link.expired
            self.links[link.userid].expires = link.expires
            self.links[link.userid].retry_count = link.retry_count

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
        self._user_store = MockUserStore()
        self._link_store = MockLinkStore()
        self._linked_account_store = MockLinkedAccount()

    def user_store(self):
        return self._user_store

    def link_store(self):
        return self._link_store

    def linked_account_store(self):
        return self._linked_account_store


class BasicAccountLinkerServiceTests(AccountLinkerAsserts):

    def setUp(self):
        self.storage_engine = MockStorageEngine()
        
    def test_init(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assertIsNotNone(mgr)

    def test_generate_key(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_key(mgr)

    def test_generate_expirary(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_expirary(mgr)

    def test_happy_path(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_happy_path(mgr)

    def test_user_client_link_already_exists(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_user_client_link_already_exists(mgr)

    def test_provided_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_provided_key_not_matched(mgr)

    def test_generated_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_not_matched(mgr)

    def test_generated_key_expired(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_expired(mgr)

    def test_lockout_after_max_retries(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_lockout_after_max_retries(mgr)

    def test_unlink_user_from_client(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client(mgr)
