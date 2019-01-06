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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.spelling import SpellingStore
from programy.storage.stores.sql.dao.corpus import Corpus
from programy.storage.entities.store import Store

class SQLSpellingStore(SQLStore, SpellingStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Corpus).delete()

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        count = success = 0

        try:
            with open(filename, "r") as text_file:
                for lines in text_file:
                    words = lines.split(' ')
                    for word in words:
                        corpus = Corpus(word=word)
                        self.storage_engine.session.add(corpus)
                        if verbose is True:
                            print(word)
                        success += 1
                        count += 1

            if commit is True:
                self.commit()

        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)

        return count, success

    def load_spelling(self, spell_checker):
        corpus = self._storage_engine.session.query(Corpus)
        words = []
        for dbword in corpus:
            words.append(dbword.word)
        all_words = " ".join(words)
        spell_checker.add_corpus(all_words)


