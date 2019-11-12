import unittest
from programy.triggers.excepter import ExceptionTrigger


class ExceptionTriggerTests(unittest.TestCase):

    def test_trigger(self):
        trigger = ExceptionTrigger()

        with self.assertRaises(Exception):
            trigger.trigger()