import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)

class BotAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BotAIMLTests.test_client = BasicTestClient()
        BotAIMLTests.test_client.bot.brain.properties.load_from_text("""
            url:http://www.keithsterling.com/aiml
            name:KeiffBot 1.0
            firstname:Keiff
            middlename:AIML
            lastname:BoT
            fullname:KeiffBot
            email:info@keiffbot.org
            gender:male
            botmaster:Keith Sterling
            organization:keithsterling.com
            version:0.0.1
            birthplace:Edinburgh, Scotland
            job:mobile virtual assistant
            species:robot
            birthday:September 9th
            birthdate:September 9th, 2016
            sign:Virgo
            logo:<img src="http://www.keithsterling.com/aiml/logo.png" width="128"/>
            religion:Atheist
            default-get:unknown
            default-property:unknown
            default-map:unknown
            learn-filename:learn.aiml
        """)

    def test_bot_property_xxx(self):
        response = BotAIMLTests.test_client.bot.ask_question("test",  "BOT PROPERTY XXX")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_url(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY URL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "http://www.keithsterling.com/aiml")

    def test_bot_property_name(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "KeiffBot 1.0")

    def test_bot_property_firstname(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY FIRSTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keiff")

    def test_bot_property_middlename(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY MIDDLENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIML")

    def test_bot_property_lastname(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY LASTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BoT")

    def test_bot_property_email(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY EMAIL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "info@keiffbot.org")

    def test_bot_property_gender(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "male")

    def test_bot_property_botmaster(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY BOTMASTER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keith Sterling")

    def test_bot_property_organisation(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY ORGANISATION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling.com")

    def test_bot_property_version(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY VERSION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "0.0.1")

    def test_bot_property_birthplace(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY BIRTHPLACE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Edinburgh, Scotland")

    def test_bot_property_birthday(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY BIRTHDAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th")

    def test_bot_property_sign(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY SIGN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Virgo")

    def test_bot_property_birthdate(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY BIRTHDATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th, 2016")

    def test_bot_property_job(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY JOB")
        self.assertIsNotNone(response)
        self.assertEqual(response, "mobile virtual assistant")

    def test_bot_property_species(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY SPECIES")
        self.assertIsNotNone(response)
        self.assertEqual(response, "robot")

    def test_bot_property_religion(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY RELIGION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "No religion, I am an Atheist")

    def test_bot_property_logo(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY LOGO")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<img src="http://www.keithsterling.com/aiml/logo.png" width="128"/>')

    def test_bot_property_default_get(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY DEFAULT GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_map(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY DEFAULT MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_property(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY DEFAULT PROPERTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_learn_filename(self):
        response = BotAIMLTests.test_client.bot.ask_question("test", "BOT PROPERTY LEARN FILENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "learn.aiml")
