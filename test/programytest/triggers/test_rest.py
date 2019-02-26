import unittest

from programy.triggers.manager import TriggerManager
from programy.triggers.config import TriggerConfiguration
from programytest.client import TestClient
from programy.triggers.rest import RestTriggerManager

class MockResponse(object):

    def __init__(self, status_code=200):
        self.status_code = status_code


class MockRestTriggerManager(RestTriggerManager):

    def __init__(self, config: TriggerConfiguration):
        RestTriggerManager.__init__(self, config)

    def post_data(self, api_url_base, headers, payload):
        return MockResponse()


class RestTriggerManagerTests(unittest.TestCase):

    def test_create(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.REST_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

    def test_trigger_triggers(self):
        config = TriggerConfiguration()
        config._manager = "programytest.triggers.test_rest.MockRestTriggerManager"
        config._additionals["url"] = "http://localhost/api/1.0/ask"

        mgr = TriggerManager.load_trigger_manager(config)

        client = TestClient()
        client_context = client.create_client_context("testid")

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(triggered)

        triggered = mgr.trigger("SYSTEM_STARTUP", additional={"key": "value"})
        self.assertTrue(triggered)

        triggered = mgr.trigger("CONVERSATION_START", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT")
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context, additional={"key": "value"})
        self.assertTrue(triggered)

