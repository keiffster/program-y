import unittest
import os
from programy.braintree import BraintreeManager
from programy.config.brain.braintree import BrainBraintreeConfiguration
from programytest.client import TestClient


class BraintreeManagerTests(unittest.TestCase):

    def test_dump_no_create(self):
        config = BrainBraintreeConfiguration()
        config._create = False
        config._save_as_user = "system"

        mgr = BraintreeManager(config)

        client = TestClient()
        client_context = client.create_client_context("testid")

        mgr.dump_brain_tree(client_context)

    def test_dump_create_no_storage(self):
        config = BrainBraintreeConfiguration()
        config._create = True
        config._save_as_user = "system"

        mgr = BraintreeManager(config)

        client = TestClient()
        client_context = client.create_client_context("testid")

        mgr.dump_brain_tree(client_context)

    def get_temp_dir(self):
        if os.name == 'posix':
            return '/tmp'
        elif os.name == 'nt':
            import tempfile
            return tempfile.gettempdir()
        else:
            raise Exception("Unknown operating system [%s]" % os.name)

    def test_dump_create_(self):
        tmpdir = self.get_temp_dir()
        brainfile = tmpdir + os.sep + "braintree.bin"

        config = BrainBraintreeConfiguration()
        config._create = True
        config._save_as_user = "system"

        mgr = BraintreeManager(config)

        if os.path.exists(brainfile):
            os.remove(brainfile)

        client = TestClient()
        client.add_braintree_store(brainfile)

        client_context = client.create_client_context("testid")

        mgr.dump_brain_tree(client_context)

        self.assertTrue(os.path.exists(brainfile))

        if os.path.exists(brainfile):
            os.remove(brainfile)
