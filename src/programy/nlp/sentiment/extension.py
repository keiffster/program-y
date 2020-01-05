"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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

    def _check_enabled(self, client_context):
        if client_context.bot.sentiment_analyser is not None:
            return "SENTIMENT ENABLED"

        else:
            return "SENTIMENT DISABLED"

    def _calc_conversation_sentiment(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)
        positivity, subjectivity = conversation.calculate_sentiment_score()
        if client_context.bot.sentiment_scores is not None:
            pos_str = client_context.bot.sentiment_scores.positivity(positivity)
            sub_str = client_context.bot.sentiment_scores.subjectivity(subjectivity)
            return "SENTIMENT FEELING %s AND %s" % (pos_str, sub_str)

        return "SENTIMENT FEELING NEUTRAL AND NEUTRAL"

    def _calc_question_sentiment(self, client_context, nth_question):
        conversation = client_context.bot.get_conversation(client_context)
        try:
            question = conversation.previous_nth_question(nth_question)

            positivity, subjectivity = question.calculate_sentinment_score()

            pos_str = client_context.bot.sentiment_scores.positivity(positivity)
            sub_str = client_context.bot.sentiment_scores.subjectivity(subjectivity)

            return "SENTIMENT FEELING %s AND %s" % (pos_str, sub_str)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to calculate sentiment", excep)
            return "SENTIMENT FEELING NEUTRAL AND NEUTRAL"

    def _calc_feeling(self, client_context, words):
        if client_context.bot.sentiment_analyser is not None:

            if len(words) >= 3:
                if words[2] == 'LAST':
                    if len(words) == 4:
                        if words[3].isdigit():
                            return self._calc_question_sentiment(client_context, int(words[3]))

                elif words[2] == 'OVERALL':
                    return self._calc_conversation_sentiment(client_context)

            return "SENTIMENT INVALID COMMAND"

        else:
            return "SENTIMENT DISABLED"

    def _current_score(self, client_context, words):

        conversation = client_context.bot.get_conversation(client_context)

        assert conversation is not None

        if len(words) == 3:

            if words[2] == 'NUMERIC':
                return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (conversation.properties['positivity'],
                                                                           conversation.properties['subjectivity'])

            if words[2] == 'TEXT':
                pos_str = client_context.bot.sentiment_scores.positivity(float(conversation.properties['positivity']),
                                                                         client_context)
                subj_str = client_context.bot.sentiment_scores.subjectivity(
                    float(conversation.properties['subjectivity']), client_context)
                return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (pos_str, subj_str)

        return "SENTIMENT INVALID COMMAND"

    def _calc_score(self, client_context, words):
        if client_context.bot.sentiment_analyser is not None:

            text = " ".join(words[2:])

            positivity, subjectivity = client_context.bot.sentiment_analyser.analyse_all(text)

            pos_str = "UNKNOWN"
            subj_str = "UNKNOWN"
            if client_context.bot.sentiment_scores is not None:
                pos_str = client_context.bot.sentiment_scores.positivity(positivity, client_context)
                subj_str = client_context.bot.sentiment_scores.subjectivity(subjectivity, client_context)

            return "SENTIMENT SCORES POSITIVITY %s SUBJECTIVITY %s" % (pos_str, subj_str)

        else:
            return "SENTIMENT DISABLED"

    def _get_positivity(self, client_context, words):
        positivity = float(words[2])
        return client_context.bot.sentiment_scores.positivity(positivity, client_context)

    def _get_subjectivity(self, client_context, words):
        subjectivity = float(words[2])
        return client_context.bot.sentiment_scores.subjectivity(subjectivity, client_context)

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Sentiment - Calling external service for with extra data [%s]", data)

        # SENTIMENT SCORE <TEXT STRING>
        # SENTIMENT FEELING <TEXT STRING>
        # SENTIMENT ENABLED
        # SENTIMENT POSITIVITY <VALUE>
        # SENTIMENT SUBJECTIVITY <VALUE>

        words = data.split(" ")
        if words[0] == "SENTIMENT":

            if len(words) >= 2:
                if words[1] == "CURRENT":
                    return self._current_score(client_context, words)

                if words[1] == "SCORE":
                    return self._calc_score(client_context, words)

                if words[1] == "FEELING":
                    return self._calc_feeling(client_context, words)

                if words[1] == 'ENABLED':
                    return self._check_enabled(client_context)

                if words[1] == 'POSITIVITY':
                    return self._get_positivity(client_context, words)

                if words[1] == 'SUBJECTIVITY':
                    return self._get_subjectivity(client_context, words)

        return "SENTIMENT INVALID COMMAND"
