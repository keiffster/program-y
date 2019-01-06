"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class SentimentScores(object):

    def positivity(self, score, client_context=None):
        # Score between -1.0 and 1.0

        if score < -0.9:
            return "EXTREMELY NEGATIVE"

        elif score > -0.9 and score <= -0.7:
            return "VERY NEGATIVE"

        elif score > -0.7 and score <= -0.5:
            return "QUITE NEGATIVE"

        elif score > -0.5 and score <= -0.3:
            return "NEGATIVE"

        elif score > -0.3 and score <= -0.1:
            return "SOMEWHAT NEGATIVE"

        elif score > -0.1 and score <= 0.1:
            return "NEUTRAL"

        elif score > 0.1 and score <= 0.3:
            return "SOMEWHAT POSITIVE"

        elif score > 0.3 and score <= 0.5:
            return "POSITIVE"

        elif score > 0.5 and score <= 0.7:
            return "QUITE POSITIVE"

        elif score > 0.7 and score <= 0.9:
            return "VERY POSITIVE"

        elif score > 0.9:
            return "EXTREMELY POSITIVE"

    def subjectivity(self, score, client_context=None):
        # Score between 0.0 and 1.0

        if score == 0.0:
            return "COMPLETELY OBJECTIVE"

        if score > 0.0 and score <= 0.2:
            return "MOSTLY OBJECTIVE"

        if score > 0.2 and score <= 0.4:
            return "SOMEWHAT OBJECTIVE"

        elif score > 0.4 and score <= 0.6:
            return "NEUTRAL"

        if score > 0.6 and score <= 0.8:
            return "SOMEWHAT SUBJECTIVE"

        if score > 0.8 and score < 1.0:
            return "MOSTLY SUBJECTIVE"

        elif score == 1.0:
            return "COMPLETELY SUBJECTIVE"