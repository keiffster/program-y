
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

    def display(self, output_func=print):
        output_func("\t-Brain------------------")
        output_func("\tclientid: [%s]"%self.clientid)
        output_func("\tsrai:     [%s]"%("True" if self.srai is True else "False"))
        output_func("\tsentence: [%s]"%self.sentence.text())
        output_func("\ttopic:    [%s]"%self.topic)
        output_func("\tthat:     [%s]"%self.that)
        output_func("\tmatches:")
        if self.match_context is not None:
            self.match_context.list_matches(output_func=output_func, tabs="\t", include_template=False)
        output_func("\tanswer:   [%s]"%self.raw_response)
        if self.oob_response is not None:
            output_func("\toob:      [%s]"%self.oob_response)
        output_func("\t------------------------")


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
        output_func("clientid: [%s]"%self.clientid)
        output_func("srai:     [%s]"%("True" if self.srai is True else "False"))
        output_func("question: [%s]"%self.raw_question)
        for brain_question_contexts in self.brain_question_contexts:
            brain_question_contexts.display(output_func=output_func)
        output_func("final:    [%s]"%self.final_response)
        output_func("-----------------------------------------------")



