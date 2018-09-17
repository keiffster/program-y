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
        self.assertEqual(user['userid'], '1')
        self.assertEqual(user['client'], "console")

        users = store.get_client_users("console")
        self.assertEqual(3, len(users))

        for user in users:
            self.assertEqual(user['client'], 'console')
