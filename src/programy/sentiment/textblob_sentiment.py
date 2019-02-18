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

from textblob import TextBlob

from programy.sentiment.base import BaseSentimentAnalyser


class TextBlobSentimentAnalyser(BaseSentimentAnalyser):

    def analyse_each(self, text):
        blob = TextBlob(text)

        sentiments = []
        for sentence in blob.sentences:
             sentiments.append((sentence.sentiment.polarity, sentence.sentiment.subjectivity))

        return sentiments

    def analyse_all(self, text):
        blob = TextBlob(text)

        polarity = 0.00
        subjectivity = 0.00
        count = 0

        for sentence in blob.sentences:
            polarity += sentence.sentiment.polarity
            subjectivity += sentence.sentiment.subjectivity
            count += 1

        if count > 0:
            polarity /= count
            subjectivity /= count
        else:
            subjectivity = 0.5

        return polarity, subjectivity
