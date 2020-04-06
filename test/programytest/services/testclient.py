import logging
from programytest.client import TestClient


class ServiceTestClient(TestClient):

    def __init__(self, debug=True, level=logging.ERROR):
        TestClient.__init__(self, debug=debug, level=level)

    def load_storage(self):
        super(ServiceTestClient, self).load_storage()
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()
