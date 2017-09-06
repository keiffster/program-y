import unittest

from programy.extensions.survey.survey import SurveyExtension

class SurveyExtensionTests(unittest.TestCase):

    def setUp(self):
        self.bot = None
        self.clientid = "testid"

    def test_survey(self):

        minutes = SurveyExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute(self.bot, self.clientid, "Answer1| Answer2")
        self.assertIsNotNone(result)
        self.assertEqual("OK", result)