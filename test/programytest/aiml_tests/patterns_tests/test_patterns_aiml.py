import unittest
import os

from programytest.client import TestClient


class PatternsTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PatternsTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class PatternsAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternsTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic2_1(self):
        response = self._client_context.bot.ask_question(self._client_context,  "A B")
        self.assertEqual(response, "C.")

    def test_basic2_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "A B C")
        self.assertEqual(response, "D.")

    def test_basic2_3_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "D E")
        self.assertEqual(response, "")

    def test_basic2_3_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "A D E")
        self.assertEqual(response, "F.")

    def test_basic2_3_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "A B C D E")
        self.assertEqual(response, "F.")

    def test_basic2_3_4(self):
        response = self._client_context.bot.ask_question(self._client_context, "X D E X")
        self.assertEqual(response, "")

    def test_basic2_4_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "G H")
        self.assertEqual(response, "")

    def test_basic2_4_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "G X H")
        self.assertEqual(response, "I.")

    def test_basic2_4_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "G X X H")
        self.assertEqual(response, "I.")

    def test_basic2_5_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "J K")
        self.assertEqual(response, "")

    #def test_basic2_5_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "J K X")
        self.assertEqual(response, "L.")

        response = self._client_context.bot.ask_question(self._client_context, "J K X X X")
        self.assertEqual(response, "L.")

    def test_basic2_6(self):
        response = self._client_context.bot.ask_question(self._client_context, "M N")
        self.assertEqual(response, "O.")

        response = self._client_context.bot.ask_question(self._client_context, "X M N")
        self.assertEqual(response, "O.")

        response = self._client_context.bot.ask_question(self._client_context, "X X X M N")
        self.assertEqual(response, "O.")

    def test_basic2_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "P Q")
        self.assertEqual(response, "R.")

        response = self._client_context.bot.ask_question(self._client_context, "P X Q")
        self.assertEqual(response, "R.")

        response = self._client_context.bot.ask_question(self._client_context, "P X X X Q")
        self.assertEqual(response, "R.")

    def test_basic2_8(self):
        response = self._client_context.bot.ask_question(self._client_context, "S T")
        self.assertEqual(response, "U.")

        response = self._client_context.bot.ask_question(self._client_context, "S T X")
        self.assertEqual(response, "U.")

        response = self._client_context.bot.ask_question(self._client_context, "S T X X X")
        self.assertEqual(response, "U.")

    # * AA BB # -> CC
    def test_basic2_9(self):
        response = self._client_context.bot.ask_question(self._client_context, "AA BB")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX AA BB")
        self.assertEqual(response, "CC.")

        response = self._client_context.bot.ask_question(self._client_context, "XX AA BB XX")
        self.assertEqual(response, "CC.")

        response = self._client_context.bot.ask_question(self._client_context, "XX XX AA BB XX XX")
        self.assertEqual(response, "CC.")

    # * CC DD * -> EE
    def test_basic2_10(self):
        response = self._client_context.bot.ask_question(self._client_context, "CC DD")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX CC DD")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "CC DD XX")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX CC DD XX")
        self.assertEqual(response, "EE.")

        response = self._client_context.bot.ask_question(self._client_context, "XX XX CC DD XX XX")
        self.assertEqual(response, "EE.")

    # # FF GG * -> HH
    def test_basic2_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "FF GG")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "FF GG XX")
        self.assertEqual(response, "HH.")

        response = self._client_context.bot.ask_question(self._client_context, "XX FF GG")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX FF GG XX")
        self.assertEqual(response, "HH.")

        response = self._client_context.bot.ask_question(self._client_context, "XX XX FF GG XX XX")
        self.assertEqual(response, "HH.")

    # # II JJ # -> KK
    def test_basic2_12(self):
        response = self._client_context.bot.ask_question(self._client_context, "II JJ")
        self.assertEqual(response, "KK.")

        response = self._client_context.bot.ask_question(self._client_context, "XX II JJ")
        self.assertEqual(response, "KK.")

        response = self._client_context.bot.ask_question(self._client_context, "XX II JJ XX")
        self.assertEqual(response, "KK.")

        response = self._client_context.bot.ask_question(self._client_context, "XX XX II JJ XX XX")
        self.assertEqual(response, "KK.")

    # * MM * MM * NN * NN * -> PPPP
    def test_basic2_13(self):
        response = self._client_context.bot.ask_question(self._client_context, "MM MM NN NN")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX MM MM NN NN")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX MM XX MM NN NN")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX MM XX MM XX NN NN")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX MM XX MM XX NN XX NN")
        self.assertEqual(response, "")

        response = self._client_context.bot.ask_question(self._client_context, "XX MM XX MM XX NN XX NN XX")
        self.assertEqual(response, "PPPP.")

    # # PP # PP # QQ # QQ # -> RRRR
    def test_basic2_14(self):
        response = self._client_context.bot.ask_question(self._client_context, "PP PP QQ QQ")
        self.assertEqual(response, "RRRR.")

        response = self._client_context.bot.ask_question(self._client_context, "XX PP PP QQ QQ")
        self.assertEqual(response, "RRRR.")

        response = self._client_context.bot.ask_question(self._client_context, "PP XX PP QQ QQ")
        self.assertEqual(response, "RRRR.")

        response = self._client_context.bot.ask_question(self._client_context, "PP PP XX QQ QQ")
        self.assertEqual(response, "RRRR.")

        response = self._client_context.bot.ask_question(self._client_context, "PP PP QQ XX QQ")
        self.assertEqual(response, "RRRR.")

        response = self._client_context.bot.ask_question(self._client_context, "PP PP QQ QQ XX")
        self.assertEqual(response, "RRRR.")
