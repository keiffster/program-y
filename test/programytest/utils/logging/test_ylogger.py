import unittest

from programy.utils.logging.ylogger import YLogger
from programy.utils.logging.ylogger import YLoggerSnapshot
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class YLoggerTests(unittest.TestCase):

    def test_ylogger(self):
        client_context = ClientContext(TestClient(), "testid")
        
        snapshot = YLoggerSnapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.critical(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.fatal(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.error(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.exception(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(0) Info(0), Debug(0)")

        YLogger.warning(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(0), Debug(0)")

        YLogger.info(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(1), Debug(0)")

        YLogger.debug(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEquals(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(1), Debug(1)")
