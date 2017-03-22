import unittest

from extensions.survey.survey import SurveyExtension

class SurveyExtensionTests(unittest.TestCase):

    def test_survey(self):

        minutes = SurveyExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute("Answer1| Answer2")
        self.assertIsNotNone(result)
        self.assertEqual("OK", result)