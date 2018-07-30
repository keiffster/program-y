import unittest

class UserStoreAsserts(unittest.TestCase):

    def assert_user_storage(self, store):
        
        store.empty()

        store.add_user('1', "console")
        store.add_user('2', "console")
        store.add_user('3', "twitter")
        store.add_user('4', "facebook")
        store.add_user('5', "console")
        store.commit()

        user = store.get_user('1')
        self.assertEquals(user['userid'], '1')
        self.assertEquals(user['client'], "console")

        users = store.get_client_users("console")
        self.assertEquals(3, len(users))

        for user in users:
            self.assertEquals(user['client'], 'console')
