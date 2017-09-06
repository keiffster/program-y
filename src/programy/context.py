
class BrainQuestionContext(object):

    def __init__(self):
        self.clientid = None
        self.srai = None
        self.sentence = None
        self.topic = None
        self.that = None
        self.match_context = None
        self.raw_response = None
        self.oob_response = None

    def display(self, output_func=print, tabs="\t"):
        output_func("%s-Brain------------------"%tabs)
        output_func("%sclientid: [%s]"%(tabs, self.clientid if self.clientid is not None else "Unknown"))
        output_func("%ssrai:     [%s]"%(tabs, ("True" if self.srai is True else "False")))
        output_func("%ssentence: [%s]"%(tabs, self.sentence.text() if self.sentence is not None else "Unknown"))
        output_func("%stopic:    [%s]"%(tabs, self.topic if self.topic is not None else "Unknown"))
        output_func("%sthat:     [%s]"%(tabs, self.that if self.that is not None else "Unknown"))
        output_func("%smatches:"%tabs)
        if self.match_context is not None:
            self.match_context.list_matches(output_func=output_func, tabs=tabs, include_template=False)
        output_func("%sanswer:   [%s]"%(tabs, self.raw_response))
        if self.oob_response is not None:
            output_func("%soob:      [%s]"%(tabs, self.oob_response))
        output_func("%s------------------------")


class BotQuestionContext(object):

    def __init__(self):
        self.clientid = None
        self.srai = None
        self.raw_question = None
        self.final_response = None
        self.brain_question_contexts = []

    def next_brain_question_context(self):
        brain_context = BrainQuestionContext()
        self.brain_question_contexts.append(brain_context)
        return brain_context

    def display(self, output_func=print):
        output_func("-Bot-------------------------------------------")
        output_func("clientid: [%s]"%(self.clientid if self.clientid is not None else "Unknown"))
        output_func("srai:     [%s]"%("True" if self.srai is True else "False"))
        output_func("question: [%s]"%(self.raw_question if self.raw_question is not None else "Unknown"))
        for brain_question_contexts in self.brain_question_contexts:
            brain_question_contexts.display(output_func=output_func)
        output_func("final:    [%s]"%(self.final_response if self.final_response is not None else "Unknown"))
        output_func("-----------------------------------------------")



