import unittest
import os
import wikipedia

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.wikipediaservice import WikipediaService

class TestBot:

    def __init__(self):
        self.license_keys = None

class MockWikipediaAPI(object):

    DISAMBIGUATIONERROR = 1
    PAGEERROR = 2
    GENERALEXCEPTION = 3

    def __init__(self, response=None, throw_exception=None):
        self._response = response
        self._throw_exception = throw_exception

    def summary(self, title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        if self._throw_exception is not None:
            if self._throw_exception == MockWikipediaAPI.DISAMBIGUATIONERROR:
                raise wikipedia.exceptions.DisambiguationError("Title", "May Refer To")
            elif self._throw_exception == MockWikipediaAPI.PAGEERROR:
                raise wikipedia.exceptions.PageError(pageid=666)
            else:
                raise Exception()
        else:
            return self._response

class WikipediaServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):
        service = WikipediaService(api=MockWikipediaAPI(response="Test Wikipedia response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test Wikipedia response", response)

    def test_ask_question_disambiguous(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.DISAMBIGUATIONERROR))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

    def test_ask_question_pageerror_exception(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.PAGEERROR))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

    def test_ask_question_general_exception(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.GENERALEXCEPTION))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)