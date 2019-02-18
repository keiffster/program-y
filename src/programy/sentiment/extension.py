"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is an example extension that allow you to call an external service to retreive the energy consumption data
of the customer. Currently contains no authentication
"""

from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension


class SentimentExtension(Extension):

    def _check_enabled(self, context):
        if context.bot.sentiment_analyser is not None:
            return "SENTIMENT ENABLED"
        else:
            return "SENTIMENT DISABLED"

    def _calc_conversation_sentiment(self, context):
        conversation = context.bot.get_conversation(context)
        positivity, subjectivity = conversation.calculate_sentiment_score()
        if context.bot.sentiment_scores is not None:
            pos_str = context.bot.sentiment_scores.positivity(positivity)
            sub_str = context.bot.sentiment_scores.subjectivity(subjectivity)
            return "SENTIMENT FEELING %s AND %s"%(pos_str, sub_str)
        return "SENTIMENT FEELING NEUTRAL AND NEUTRAL"

    def _calc_question_sentiment(self, context, nth_question):
        conversation = context.bot.get_conversation(context)
        try:
            sentence = conversation.previous_nth_question(nth_question)
            pos_str = context.bot.sentiment_scores.positivity(sentence.positivity)
            sub_str = context.bot.sentiment_scores.subjectivity(sentence.subjectivity)
            return "SENTIMENT FEELING %s AND %s" % (pos_str, sub_str)
        except:
            print("Whoops")
            return "SENTIMENT FEELING NEUTRAL AND NEUTRAL"

    def _calc_feeling(self, context, words):
        if context.bot.sentiment_analyser is not None:

            if len(words) >= 3:
                if words[2] == 'LAST':
                    if len(words) == 4:
                        if words[3].isdigit():
                            return self._calc_question_sentiment(context, int(words[3]))

                elif words[2] == 'OVERALL':
                    return self._calc_conversation_sentiment(context)

            return "SENTIMENT INVALID COMMAND"

        else:
            return "SENTIMENT DISABLED"

    def _current_score(self, context, words):

        conversation = context.bot.get_conversation(context)

        assert (conversation is not None)

        if len(words) == 3:

            if words[2] == 'NUMERIC':
                return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (conversation.properties['positivity'], conversation.properties['subjectivity'])

            if words[2] == 'TEXT':
                pos_str = context.bot.sentiment_scores.positivity(float(conversation.properties['positivity']), context)
                subj_str = context.bot.sentiment_scores.subjectivity(float(conversation.properties['subjectivity']), context)
                return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (pos_str, subj_str)

        return "SENTIMENT INVALID COMMAND"

    def _calc_score(self, context, words):
        if context.bot.sentiment_analyser is not None:

            text = " ".join(words[2:])

            positivity, subjectivity = context.bot.sentiment_analyser.analyse_all(text)

            pos_str = "UNKNOWN"
            subj_str = "UNKNOWN"
            if context.bot.sentiment_scores is not None:
                pos_str = context.bot.sentiment_scores.positivity(positivity, context)
                subj_str = context.bot.sentiment_scores.subjectivity(subjectivity, context)

            return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (pos_str, subj_str)

        else:
            return "SENTIMENT DISABLED"

    def _get_positivity(self, context, words):
        positivity = float(words[2])
        return context.bot.sentiment_scores.positivity(positivity, context)

    def _get_subjectivity(self, context, words):
        subjectivity = float(words[2])
        return context.bot.sentiment_scores.subjectivity(subjectivity, context)

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "Sentiment - Calling external service for with extra data [%s]", data)

        # SENTIMENT SCORE <TEXT STRING>
        # SENTIMENT FEELING <TEXT STRING>
        # SENTIMENT ENABLED
        # SENTIMENT POSITIVITY <VALUE>
        # SENTIMENT SUBJECTIVITY <VALUE>

        words = data.split(" ")
        if words:

            if words[0] == "SENTIMENT":

                if len(words) >= 2:
                    if words[1] == "CURRENT":
                        return self._current_score(context, words)

                    if words[1] == "SCORE":
                        return self._calc_score(context, words)

                    if words[1] == "FEELING":
                        return self._calc_feeling(context, words)

                    if words[1] == 'ENABLED':
                        return self._check_enabled(context)

                    if words[1] == 'POSITIVITY':
                        return self._get_positivity(context, words)

                    if words[1] == 'SUBJECTIVITY':
                        return self._get_subjectivity(context, words)

        return "SENTIMENT INVALID COMMAND"

