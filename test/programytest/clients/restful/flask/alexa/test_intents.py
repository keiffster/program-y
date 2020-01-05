import os
import unittest

from programy.clients.restful.flask.alexa.intents import CancelIntent
from programy.clients.restful.flask.alexa.intents import HelpIntent
from programy.clients.restful.flask.alexa.intents import IntentGenerator
from programy.clients.restful.flask.alexa.intents import Intents
from programy.clients.restful.flask.alexa.intents import InteractionModel
from programy.clients.restful.flask.alexa.intents import LanguageModel
from programy.clients.restful.flask.alexa.intents import QueryIntent
from programy.clients.restful.flask.alexa.intents import StopIntent


class CancelIntentTests(unittest.TestCase):

    def test_generate(self):
        intent = CancelIntent()
        data = intent.generate()
        self.assertIsNotNone(data)

        self.assertTrue("name" in data)
        self.assertEqual(data['name'], "AMAZON.CancelIntent")

        self.assertFalse("slots" in data)

        self.assertTrue("samples" in data)
        samples = data['samples']
        self.assertEqual(0, len(samples))


class HelpIntentTests(unittest.TestCase):

    def test_generate(self):
        intent = HelpIntent()
        data = intent.generate()
        self.assertIsNotNone(data)

        self.assertTrue("name" in data)
        self.assertEqual(data['name'], "AMAZON.HelpIntent")

        self.assertFalse("slots" in data)

        self.assertTrue("samples" in data)
        samples = data['samples']
        self.assertEqual(0, len(samples))


class StopIntentTests(unittest.TestCase):

    def test_generate(self):
        intent = StopIntent()
        data = intent.generate()
        self.assertIsNotNone(data)

        self.assertTrue("name" in data)
        self.assertEqual(data['name'], "AMAZON.StopIntent")

        self.assertFalse("slots" in data)

        self.assertTrue("samples" in data)
        samples = data['samples']
        self.assertEqual(0, len(samples))


class QueryIntentTests(unittest.TestCase):

    def test_generate(self):
        intent = QueryIntent("test")
        self.assertIsNotNone(intent)

        data = intent.generate()
        self.assertIsNotNone(data)

        self.assertTrue("name" in data)
        self.assertEqual(data['name'], "AskTest")

        self.assertTrue("slots" in data)
        self.assertEqual(1, len(data['slots']))
        slot = data['slots'][0]
        self.assertIsNotNone(slot)
        self.assertTrue("name" in slot)
        self.assertEqual(slot['name'], 'text')
        self.assertEqual(slot['type'], "AMAZON.SearchQuery")

        self.assertTrue("samples" in data)
        samples = data['samples']
        self.assertEqual(1, len(samples))
        self.assertEqual(samples[0], "test {text}")


class LanguageModelTests(unittest.TestCase):

    def test_generate(self):
        intents = [CancelIntent(), HelpIntent(), StopIntent()]
        model = LanguageModel("test skill", intents)
        self.assertIsNotNone(model)

        data = model.generate()
        self.assertIsNotNone(data)


class InteractionModelTests(unittest.TestCase):

    def test_generate(self):
        intents = [CancelIntent(), HelpIntent(), StopIntent()]
        language_model = LanguageModel("test skill", intents)
        model = InteractionModel(language_model)
        self.assertIsNotNone(model)

        data = model.generate()
        self.assertIsNotNone(data)


class IntentsTests(unittest.TestCase):

    def test_generate(self):
        intents = [CancelIntent(), HelpIntent(), StopIntent(), QueryIntent('Ask')]
        language_model = LanguageModel("test skill", intents)
        interaction_model = InteractionModel(language_model)
        intents = Intents(interaction_model)
        self.assertIsNotNone(intents)

        data = intents.generate()
        self.assertIsNotNone(data)

        self.assertTrue('interactionModel' in data)
        interactionModel = data['interactionModel']
        self.assertIsNotNone(interactionModel)

        self.assertTrue('languageModel' in interactionModel)
        languageModel = interactionModel['languageModel']
        self.assertIsNotNone(languageModel)

        self.assertTrue('invocationName' in languageModel)
        self.assertTrue('intents' in languageModel)
        intents = languageModel['intents']
        self.assertIsNotNone(intents)
        self.assertEqual(4, len(intents))


class IntentGeneratorTests(unittest.TestCase):
    
    def test_generate(self):

        system_intents = [CancelIntent(), HelpIntent(), StopIntent()]
        intents_word_file = os.path.dirname(__file__) + os.sep + "intents.txt"
        intents_json_file = os.path.dirname(__file__) + os.sep + "intents.json.tmp"
        intents_mapping_file = os.path.dirname(__file__) + os.sep + "intents.maps.tmp"

        if os.path.exists(intents_json_file) is True:
            os.remove(intents_json_file)
        self.assertFalse(os.path.exists(intents_json_file))

        if os.path.exists(intents_mapping_file) is True:
            os.remove(intents_mapping_file)
        self.assertFalse(os.path.exists(intents_mapping_file))

        generator = IntentGenerator("test intents", system_intents, intents_word_file, intents_json_file, intents_mapping_file)
        generator.generate()

        self.assertTrue(os.path.exists(intents_json_file))
        if os.path.exists(intents_json_file) is True:
            os.remove(intents_json_file)

        self.assertTrue(os.path.exists(intents_mapping_file))
        if os.path.exists(intents_mapping_file) is True:
            os.remove(intents_mapping_file)
