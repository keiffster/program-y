import unittest
import logging

from test.custom import CustomAssertions

class TestProperties:

    def __init__(self):
        self._properties = {}

    def set_property(self, name, value):
        self._properties[name] = value

    def has_property(self, name):
        if name in self._properties:
            return True
        else:
            return False

    def property(self, name):
        return self._properties[name]

class TestSet:

    def __init__(self):
        self._sets = {}

    def add_set(self, name, values):
        self._sets[name] = values

    def contains(self, name):
        if name in self._sets:
            return True
        else:
            return False

    def set(self, name):
        return self._sets[name]

class TestBrain:

    def __init__(self):
        self.sets = TestSet()
        self.properties = TestProperties()

class TestBot:

    def __init__(self):
        self.brain = TestBrain()

class PatternTestBaseClass(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.bot = TestBot()
        self.clientid = "testid"

