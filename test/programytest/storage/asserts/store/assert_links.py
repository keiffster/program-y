import unittest
import datetime

class LinkStoreAsserts(unittest.TestCase):

    def assert_links_storage(self, store):

        store.empty()

        store.create_link('user1', 'Password123', 'ABCDEF', expires=datetime.datetime.now())
        store.create_link('user2', 'Password123', 'ABCDEF', expires=datetime.datetime.now())

        self.assertTrue(store.link_exists('user1', 'Password123', 'ABCDEF'))
        self.assertFalse(store.link_exists('user99', 'Password123', 'ABCDEF'))

        link = store.get_link('user1')
        self.assertIsNotNone(link)
        self.assertEqual('user1', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        link = store.get_link('user2')
        self.assertIsNotNone(link)
        self.assertEqual('user2', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        store.remove_link('user1')
        store.commit()
        link = store.get_link('user1')
        self.assertIsNone(link)

        link = store.get_link('user2')
        self.assertIsNotNone(link)
        self.assertEqual('user2', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        link.expired = True
        store.update_link(link)