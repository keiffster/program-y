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
"""
from programy.extensions.base import Extension
from programy.nlp.synsets.synsets import Synsets
from programy.utils.logging.ylogger import YLogger


class SynsetsExtension(Extension):

    def __init__(self):
        self._synsets = Synsets()

    def _get_similarities(self, word1, word2, weight):
        results = self._synsets.get_similarity(word1, word2)
        for result in results:
            if result[2] >= weight:
                return True

        return False

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        del client_context

        words = data.split(" ")
        if words[0] == 'SIMILAR':
            if len(words) == 3:
                word1 = words[1]
                word2 = words[2]
                weight = 0.00
            elif len(words) == 6:
                word1 = words[1]
                word2 = words[2]
                weight = float("%s.%s" % (words[3], words[5]))
            else:
                return "FALSE"

            try:
                if self._get_similarities(word1, word2, weight) is True:
                    return "TRUE"

            except Exception as e:
                YLogger.exception_nostack(self, "Failed to get similarity", e)

        elif words[0] == 'SIMILARS':

            if len(words) == 3:
                word_type = words[1]
                word = words[2]

                if word_type == 'WORDS':
                    results = self._synsets.get_similar_words(word)
                elif word_type == 'VERBS':
                    results = self._synsets.get_similar_verbs(word)
                elif word_type == 'NOUNS':
                    results = self._synsets.get_similar_nouns(word)
                elif word_type == 'ADJECTIVES':
                    results = self._synsets.get_similar_adjectives(word)
                elif word_type == 'ADVERBS':
                    results = self._synsets.get_similar_adverbs(word)
                else:
                    return "FALSE"

                return "TRUE %s" % " ".join([word.upper() for word in results])

        return "FALSE"
