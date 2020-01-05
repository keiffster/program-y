import unittest
from programy.utils.logging.ylogger import YLoggerSnapshot


class YLoggerSnapshotTests(unittest.TestCase):

    def test_snapshot_with_defaults(self):

        snapshot = YLoggerSnapshot()

        self.assertIsNotNone(snapshot)
        self.assertEquals("Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)", str(snapshot))
        self.assertEqual({'criticals': 0,
                          'debugs': 0,
                          'errors': 0,
                          'exceptions': 0,
                          'fatals': 0,
                          'infos': 0,
                          'warnings': 0}, snapshot.to_json())

    def test_snapshot_without_defaults(self):

        snapshot = YLoggerSnapshot(criticals=1, fatals=2, errors=3, exceptions=4, warnings=5, infos=6, debugs=7)

        self.assertIsNotNone(snapshot)
        self.assertEquals("Critical(1) Fatal(2) Error(3) Exception(4) Warning(5) Info(6), Debug(7)", str(snapshot))
        self.assertEqual({'criticals': 1,
                          'debugs': 7,
                          'errors': 3,
                          'exceptions': 4,
                          'fatals': 2,
                          'infos': 6,
                          'warnings': 5}, snapshot.to_json())

