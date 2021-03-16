import logging
import os
from programytest.client import TestClient
from programytest.externals import integration_tests_active


class ServiceTestClient(TestClient):

    RELATIVE_PATH = "testdata"

    def __init__(self, debug=True, level=logging.ERROR):
        TestClient.__init__(self, debug=debug, level=level)

    def get_license_key_file(self):
        if integration_tests_active() is True:
            return os.path.dirname(__file__) + os.sep + ServiceTestClient.RELATIVE_PATH + os.sep + "license.keys"

        else:
            return os.path.dirname(__file__) + os.sep + ServiceTestClient.RELATIVE_PATH + os.sep + "test_licenses.keys"

    def load_storage(self):
        super(ServiceTestClient, self).load_storage()
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()
        self.add_license_keys_store(filepath=self.get_license_key_file())

