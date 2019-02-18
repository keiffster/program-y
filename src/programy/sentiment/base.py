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
from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader


class BaseSentimentAnalyser(object):

    def initialise(self, storage_factory=None):
        pass

    def analyse_each(self, text):
        raise NotImplementedError()

    def analyse_all(self, text):
        raise NotImplementedError()

    @staticmethod
    def initiate_sentiment_analyser(sentiment_config):
        if sentiment_config.classname is not None:
            analyser = None
            scores = None

            try:
                YLogger.info(None, "Loading sentiment analyser from class [%s]", sentiment_config.classname)
                sentiment_class = ClassLoader.instantiate_class(sentiment_config.classname)
                analyser = sentiment_class()
                analyser.initialise()

            except Exception as excep:
                YLogger.exception(None, "Failed to initiate sentiment analyser", excep)

            try:
                YLogger.info(None, "Loading sentiment scores from class [%s]", sentiment_config.classname)
                scores_class = ClassLoader.instantiate_class(sentiment_config.scores)
                scores = scores_class()

            except Exception as excep:
                YLogger.exception(None, "Failed to initiate sentiment analyser", excep)

            return analyser, scores

        else:
            YLogger.warning(None, "No configuration setting for sentiment analyser!")

        return None, None
