"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.dynamic.sets.set import DynamicSet
from programy.utils.logging.ylogger import YLogger
from programy.nlp.synsets.synsets import Synsets


class IsSynset(DynamicSet):
    NAME = "SYNSET"
    SIMILAR = 'similar'

    def __init__(self, config):
        DynamicSet.__init__(self, config)
        self._synset = Synsets()

    def is_member(self, client_context, value, additional=None):
        if value is not None:
            if additional is not None:
                if IsSynset.SIMILAR in additional:
                    similar = additional[IsSynset.SIMILAR]

                    similars = self._synset.get_similar_words(similar)
                    for word in similars:
                        if word.upper() == value.upper():
                            return True

                else:
                    YLogger.error(self, "Missing 'similar' attribute passed to IsSynset.is_member!")

            else:
                YLogger.error(self, "Missing additional parameters passed to IsSynset.is_member!")

        else:
            YLogger.error(self, "None value passed to IsSynset.is_member!")

        return False
