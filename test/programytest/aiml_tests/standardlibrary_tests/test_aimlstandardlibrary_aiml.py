import unittest
import os

from programytest.client import TestClient


class StandardLibraryTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(StandardLibraryTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class StandardLibraryAIMLTests(unittest.TestCase):

    def setUp(self):
        client = StandardLibraryTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.bot.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

    def test_xfalse(self):
        response = self._client_context.bot.ask_question(self._client_context, "XFALSE TEST")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xtrue(self):
        response = self._client_context.bot.ask_question(self._client_context, "XTRUE TEST")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xnumber(self):
        response = self._client_context.bot.ask_question(self._client_context, "XNUMBER 666")
        self.assertIsNotNone(response)
        self.assertEqual('666.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XNUMBER XXX")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xstring(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSTRING 666")
        self.assertIsNotNone(response)
        self.assertEqual('666.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XSTRING XXX")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xistrue(self):
        response = self._client_context.bot.ask_question(self._client_context, "XISTRUE TRUE")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XISTRUE FALSE")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xisfalse(self):
        response = self._client_context.bot.ask_question(self._client_context, "XISFALSE TRUE")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XISFALSE FALSE")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xisnumber(self):
        response = self._client_context.bot.ask_question(self._client_context, "XISNUMBER 6666")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XISNUMBER XXXX")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xistypeof(self):
        response = self._client_context.bot.ask_question(self._client_context, "XTYPEOF 6666")
        self.assertIsNotNone(response)
        self.assertEqual('XNUMBER.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XTYPEOF TRUE")
        self.assertIsNotNone(response)
        self.assertEqual('XBOOL.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XTYPEOF FALSE")
        self.assertIsNotNone(response)
        self.assertEqual('XBOOL.', response)

        response = self._client_context.bot.ask_question(self._client_context, "XTYPEOF XXXX")
        self.assertIsNotNone(response)
        self.assertEqual('XSTRING.', response)

    def test_xadd_0_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XADD 0 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xadd_1_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XADD 1 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('8.', response)

    def test_xsub_0_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUB 0 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xsub_7_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUB 7 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('7.', response)

    def test_xsub_4_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUB 4 XS 3")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xmul_1_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMUL 1 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xmul_2_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMUL 2 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('14.', response)

    def test_xdiv_0_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XDIV 0 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('Undefined.', response)

    def test_xdiv_4_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XDIV 4 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('Infinite.', response)

    def test_xdiv_4_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "XDIV 4 XS 2")
        self.assertIsNotNone(response)
        self.assertEqual('2.', response)

    def test_xmod_0_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMOD 0 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('Undefined.', response)

    def test_xmod_4_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMOD 4 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('Infinite.', response)

    def test_xmod_4_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMOD 4 XS 2")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xmod_5_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMOD 5 XS 2")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xlt_0_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 0 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xlt_7_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 7 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xlt_0_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 0 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xlt_3_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 3 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xlt_7_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 7 XS 3")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xlt_7_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLT 7 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xgt_0_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 0 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xgt_7_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 7 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xgt_0_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 0 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xgt_3_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 3 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xgt_7_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 7 XS 3")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xgt_7_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGT 7 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xle_7_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLE 7 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xle_1_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLE 1 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xle_7_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLE 7 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xge_7_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGE 7 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xge_1_7(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGE 1 XS 7")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xge_7_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XGE 7 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xadd_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XADD THIS XS THAT")
        self.assertIsNotNone(response)
        self.assertEqual('THIS THAT.', response)

    def test_xeq_string_false(self):
        response = self._client_context.bot.ask_question(self._client_context, "XEQ THIS XS THAT")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xeq_string_true(self):
        response = self._client_context.bot.ask_question(self._client_context, "XEQ THIS XS THIS")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xne_string_true(self):
        response = self._client_context.bot.ask_question(self._client_context, "XNE THIS XS THAT")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xne_string_false(self):
        response = self._client_context.bot.ask_question(self._client_context, "XNE THIS XS THIS")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_xnot_false(self):
        response = self._client_context.bot.ask_question(self._client_context, "XNOT FALSE")
        self.assertIsNotNone(response)
        self.assertEqual('TRUE.', response)

    def test_xnot_true(self):
        response = self._client_context.bot.ask_question(self._client_context, "XNOT TRUE")
        self.assertIsNotNone(response)
        self.assertEqual('FALSE.', response)

    def test_length_no_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLENGTH")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xxlength_1char_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XXLENGTH X XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xxlength_3char_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XXLENGTH X Y Z XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('3.', response)

    def test_xrandom(self):
        response = self._client_context.bot.ask_question(self._client_context, "XRANDOM")
        self.assertIsNotNone(response)
        self.assertIn(response, ['0.', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'])

    def test_xsubstring_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUBSTRING FRED XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('FRED.', response)

    def test_xsubstring_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUBSTRING FRED XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('RED.', response)

    def test_xsubstring_9(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUBSTRING FRED XS 9")
        self.assertIsNotNone(response)
        self.assertEqual('D.', response)

    def test_xsubstring_0_0(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUBSTRING FRED XS 0 XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('F.', response)

    def test_xsubstring_0_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "XSUBSTRING FRED XS 0 XS 2")
        self.assertIsNotNone(response)
        self.assertEqual('F R.', response)

    def test_xmax_999(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMAX 999")
        self.assertIsNotNone(response)
        self.assertEqual('999.', response)

    def test_xmax_11_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMAX 11 11")
        self.assertIsNotNone(response)
        self.assertEqual('11.', response)

    def test_xmax_22_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMAX 22 11")
        self.assertIsNotNone(response)
        self.assertEqual('22.', response)

    def test_xmax_11_22(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMAX 11 22")
        self.assertIsNotNone(response)
        self.assertEqual('22.', response)

    def test_xmax_11_22_33(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMAX 33 10 22")
        self.assertIsNotNone(response)
        self.assertEqual('33.', response)

    def test_xmin_999(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMIN 999")
        self.assertIsNotNone(response)
        self.assertEqual('999.', response)

    def test_xmin_11_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMIN 11 11")
        self.assertIsNotNone(response)
        self.assertEqual('11.', response)

    #def test_xmin_11_22(self):
    #    response = self._client_context.bot.ask_question(self._client_context, "XMIN 11 22")
    #    self.assertIsNotNone(response)
    #    self.assertEqual('11.', response)

    def test_xmin_22_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMIN 22 11")
        self.assertIsNotNone(response)
        self.assertEqual('11.', response)

    def test_xmin_11_22_33(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMIN 11 22 33")
        self.assertIsNotNone(response)
        self.assertEqual('11.', response)

    def test_xmin_33_22_11(self):
        response = self._client_context.bot.ask_question(self._client_context, "XMIN 33 22 11")
        self.assertIsNotNone(response)
        self.assertEqual('11.', response)

    def test_xcar_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCAR XXX")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xcar_xxx_yyy(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCAR XXX YYY")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xcar_xxx_yyy_zzz(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCAR XXX YYY ZZZ")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xcdr_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCDR XXX")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xcdr_xxx_yyy(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCDR XXX YYY")
        self.assertIsNotNone(response)
        self.assertEqual('YYY.', response)

    def test_xcdr_xxx_yyy_zzz(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCDR XXX YYY ZZZ")
        self.assertIsNotNone(response)
        self.assertEqual('YYY ZZZ.', response)

    def test_ximplode_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIMPLODE XXX")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_ximplode_xxx_yyy_zzz(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIMPLODE XXX YYY ZZZ")
        self.assertIsNotNone(response)
        self.assertEqual('XXXYYYZZZ.', response)

    def test_xreverse_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context, "XREVERSE XXX")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xreverse_xxx_yyy_zzz(self):
        response = self._client_context.bot.ask_question(self._client_context, "XREVERSE XXX YYY ZZZ")
        self.assertIsNotNone(response)
        self.assertEqual('ZZZ YYY XXX.', response)

    def test_xblackhole(self):
        response = self._client_context.bot.ask_question(self._client_context, "XBLACKHOLE")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xblackhole_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context, "XBLACKHOLE XXX")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xloop_loop(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP [ XXX ] XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xloop_loop_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP [ XLENGTH 1 ] XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xloop_loop_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP [ XLENGTH 1 ] XS 3")
        self.assertIsNotNone(response)
        self.assertEqual('1 1 1.', response)

    def test_xloop_repeat(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP XXX XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xloop_repeat_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP XXX XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('XXX.', response)

    def test_xloop_repeat_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLOOP XXX XS 3")
        self.assertIsNotNone(response)
        self.assertEqual('XXX XXX XXX.', response)

    def test_xif_then_true(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIF [ XISNUMBER 3 ] XS [ XCOUNT 1 2 3 ]")
        self.assertIsNotNone(response)
        self.assertEqual('3.', response)

    def test_xif_then_false(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIF [ XISNUMBER X ] XS [ XCOUNT 1 2 3 ]")
        self.assertIsNotNone(response)
        self.assertEqual('', response)

    def test_xif_then_else_true(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIF [ XISNUMBER 3 ] XS [ XCOUNT 1 2 3 ] XS [ XCOUNT 1 2 3 4 ]")
        self.assertIsNotNone(response)
        self.assertEqual('3.', response)

    def test_xif_then_else_false(self):
        response = self._client_context.bot.ask_question(self._client_context, "XIF [ XISNUMBER X ] XS [ XCOUNT 1 2 3 ] XS [ XCOUNT 1 2 3 4 ]")
        self.assertIsNotNone(response)
        self.assertEqual('4.', response)

    def test_xcount(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCOUNT")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xcount_3(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCOUNT 3")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xcount_3_2_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XCOUNT 3 2 1")
        self.assertIsNotNone(response)
        self.assertEqual('3.', response)
