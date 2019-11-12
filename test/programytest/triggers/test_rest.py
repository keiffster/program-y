import unittest

from programy.triggers.config import TriggerConfiguration
from programy.triggers.manager import TriggerManager
from programy.triggers.rest import RestTriggerManager
from programytest.client import TestClient


class MockResponse(object):

    def __init__(self, status_code=200):
        self.status_code = status_code


class MockRestTriggerManager(RestTriggerManager):

    def __init__(self, config: TriggerConfiguration, doexcept=False, status_code=200):
        RestTriggerManager.__init__(self, config)
        self.doexcept = doexcept
        self._status_code = status_code
        self._api_url_base = None
        self._headers = None
        self._payload = None

    def post_data(self, api_url_base, headers, payload):
        if self.doexcept is True:
            raise Exception("Mock Exception")

        self._api_url_base = api_url_base
        self._headers = headers
        self._payload = payload

        return MockResponse(self._status_code)


class RestTriggerManagerTests(unittest.TestCase):

    def test_load_trigger_manager(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.REST_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

    def test_load_trigger_manager_no_config(self):
        config = TriggerConfiguration()
        config._manager = None

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNone(mgr)

    def test_load_trigger_manager_bad_manager(self):
        config = TriggerConfiguration()
        config._manager = "some.class.or.other"

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNone(mgr)

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

    def test_trigger_triggers_exception(self):
        config = TriggerConfiguration()

        mgr = MockRestTriggerManager(config, doexcept=True)

        triggered = mgr.trigger("SYSTEM_STARTUP", client_context=None)
        self.assertFalse(triggered)

    def test_trigger_triggers_status_code_500(self):
        config = TriggerConfiguration()

        mgr = MockRestTriggerManager(config, status_code=500)

        triggered = mgr.trigger("SYSTEM_STARTUP", client_context=None)
        self.assertFalse(triggered)

    def test_trigger_with_additionals(self):
        config = TriggerConfiguration()
        config._additionals['url'] = "http://some.service.com"
        config._additionals['method'] = "POST"
        config._additionals['token'] = "ABCDEFGHIJK"

        mgr = MockRestTriggerManager(config)

        mgr.trigger("SYSTEM_STARTUP")

        self.assertEquals("http://some.service.com", mgr._api_url_base)
        self.assertEquals({'Authorisation': 'Bearer ABCDEFGHIJK', 'Content-Type': 'application/json'}, mgr._headers)
        self.assertEquals({'event': 'SYSTEM_STARTUP'}, mgr._payload)

    def test_trigger_with_additionals_no_token(self):
        config = TriggerConfiguration()
        config._additionals['url'] = "http://some.service.com"
        config._additionals['method'] = "POST"

        mgr = MockRestTriggerManager(config)

        mgr.trigger("SYSTEM_STARTUP")

        self.assertEquals("http://some.service.com", mgr._api_url_base)
        self.assertEquals({'Content-Type': 'application/json'}, mgr._headers)
        self.assertEquals({'event': 'SYSTEM_STARTUP'}, mgr._payload)

    def test_trigger_with_additionals_no_method(self):
        config = TriggerConfiguration()
        config._additionals['url'] = "http://some.service.com"
        config._additionals['method'] = "POST"

        mgr = MockRestTriggerManager(config)

        result = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(result)

    def test_trigger_with_additionals_method_get(self):
        config = TriggerConfiguration()
        config._additionals['url'] = "http://some.service.com"
        config._additionals['method'] = "GET"

        mgr = MockRestTriggerManager(config)

        result = mgr.trigger("SYSTEM_STARTUP")
        self.assertFalse(result)
