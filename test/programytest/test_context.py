import unittest

from programy.context import BrainQuestionContext
from programy.context import BotQuestionContext

str = ""

def output_func(text):
    global str
    str += text

class BrainQuestionContextTests(unittest.TestCase):

    def test_init(self):
        global str

        context = BrainQuestionContext()
        self.assertIsNotNone(context)
        self.assertIsNone(context.clientid)
        self.assertIsNone(context.srai)
        self.assertIsNone(context.sentence)
        self.assertIsNone(context.topic)
        self.assertIsNone(context.that)
        self.assertIsNone(context.match_context)
        self.assertIsNone(context.raw_response)
        self.assertIsNone(context.oob_response)

        str = ""
        context.display(output_func=output_func, tabs="")
        self.assertEquals("-Brain------------------clientid: [Unknown]srai:     [False]sentence: [Unknown]topic:    [Unknown]that:     [Unknown]matches:answer:   [None]%s------------------------", str)


class BotQuestionContextTests(unittest.TestCase):
    
    def test_init(self):
        global str

        context = BotQuestionContext()
        self.assertIsNotNone(context)
        self.assertIsNone(context.clientid)
        self.assertIsNone(context.srai)
        self.assertIsNone(context.raw_question)
        self.assertIsNone(context.final_response)
        self.assertIsNotNone(context.brain_question_contexts)

        self.assertEqual([], context.brain_question_contexts)
        question_context1 = context.next_brain_question_context()
        self.assertIsNotNone(question_context1)
        self.assertEqual([question_context1], context.brain_question_contexts)
        question_context2 = context.next_brain_question_context()
        self.assertIsNotNone(question_context2)
        self.assertEqual([question_context1, question_context2], context.brain_question_contexts)

        str = ""
        context.display(output_func=output_func)
        self.assertEquals("-Bot-------------------------------------------clientid: [Unknown]srai:     [False]question: [Unknown]	-Brain------------------	clientid: [Unknown]	srai:     [False]	sentence: [Unknown]	topic:    [Unknown]	that:     [Unknown]	matches:	answer:   [None]%s------------------------	-Brain------------------	clientid: [Unknown]	srai:     [False]	sentence: [Unknown]	topic:    [Unknown]	that:     [Unknown]	matches:	answer:   [None]%s------------------------final:    [Unknown]-----------------------------------------------", str)
