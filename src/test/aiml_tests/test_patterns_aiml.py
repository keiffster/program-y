import unittest
import logging

from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class PatternsTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(PatternsTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/patterns", ".aiml", False)

class PatternsAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PatternsAIMLTests.test_client = PatternsTestClient()
        #PatternsAIMLTests.test_client.bot.brain._aiml_parser.pattern_parser._root_node.dump("", output_func=logging.debug)

    def test_basic2_1(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test",  "A B")
        self.assertEqual(response, "C")

    def test_basic2_2(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "A B C")
        self.assertEqual(response, "D")

    def test_basic2_3(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "D E")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "A D E")
        self.assertEqual(response, "F")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "A B C D E")
        self.assertEqual(response, "F")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "X D E X")
        self.assertEqual(response, "")

    def test_basic2_4(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "G H")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "G X H")
        self.assertEqual(response, "I")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "G X X H")
        self.assertEqual(response, "I")

    def test_basic2_5(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "J K")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "J K X")
        self.assertEqual(response, "L")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "J K X X X")
        self.assertEqual(response, "L")

    def test_basic2_6(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "M N")
        self.assertEqual(response, "O")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "X M N")
        self.assertEqual(response, "O")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "X X X M N")
        self.assertEqual(response, "O")

    def test_basic2_7(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "P Q")
        self.assertEqual(response, "R")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "P X Q")
        self.assertEqual(response, "R")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "P X X X Q")
        self.assertEqual(response, "R")

    def test_basic2_8(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "S T")
        self.assertEqual(response, "U")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "S T X")
        self.assertEqual(response, "U")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "S T X X X")
        self.assertEqual(response, "U")

    # * AA BB # -> CC
    def test_basic2_9(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "AA BB")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX AA BB")
        self.assertEqual(response, "CC")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX AA BB XX")
        self.assertEqual(response, "CC")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX XX AA BB XX XX")
        self.assertEqual(response, "CC")

    # * CC DD * -> EE
    def test_basic2_10(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "CC DD")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX CC DD")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "CC DD XX")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX CC DD XX")
        self.assertEqual(response, "EE")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX XX CC DD XX XX")
        self.assertEqual(response, "EE")

    # # FF GG * -> HH
    def test_basic2_11(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "FF GG")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "FF GG XX")
        self.assertEqual(response, "HH")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX FF GG")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX FF GG XX")
        self.assertEqual(response, "HH")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX XX FF GG XX XX")
        self.assertEqual(response, "HH")

    # # II JJ # -> KK
    def test_basic2_12(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "II JJ")
        self.assertEqual(response, "KK")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX II JJ")
        self.assertEqual(response, "KK")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX II JJ XX")
        self.assertEqual(response, "KK")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX XX II JJ XX XX")
        self.assertEqual(response, "KK")

    # * MM * MM * NN * NN * -> PPPP
    def test_basic2_13(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "MM MM NN NN")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX MM MM NN NN")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX MM XX MM NN NN")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX MM XX MM XX NN NN")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX MM XX MM XX NN XX NN")
        self.assertEqual(response, "")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX MM XX MM XX NN XX NN XX")
        self.assertEqual(response, "PPPP")

    # # PP # PP # QQ # QQ # -> RRRR
    def test_basic2_14(self):
        response = PatternsAIMLTests.test_client.bot.ask_question("test", "PP PP QQ QQ")
        self.assertEqual(response, "RRRR")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "XX PP PP QQ QQ")
        self.assertEqual(response, "RRRR")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "PP XX PP QQ QQ")
        self.assertEqual(response, "RRRR")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "PP PP XX QQ QQ")
        self.assertEqual(response, "RRRR")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "PP PP QQ XX QQ")
        self.assertEqual(response, "RRRR")

        response = PatternsAIMLTests.test_client.bot.ask_question("test", "PP PP QQ QQ XX")
        self.assertEqual(response, "RRRR")
