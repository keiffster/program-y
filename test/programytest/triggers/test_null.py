import unittest
from programy.triggers.null import NullTrigger


class NullTriggerTests(unittest.TestCase):

    def test_trigger(self):
        trigger = NullTrigger()
        trigger.trigger()

    def test_trigger_additiona_no_event(self):
        trigger = NullTrigger()
        trigger.trigger(additional={})

    def test_trigger_additional_event(self):
        trigger = NullTrigger()
        trigger.trigger(additional={'event': "NULL_EVENT"})