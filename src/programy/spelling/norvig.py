#http://norvig.com/spell-correct.html

import re
import os
from programy.utils.logging.ylogger import YLogger
from collections import Counter

from programy.spelling.base import SpellingChecker

class NorvigSpellingChecker(SpellingChecker):

    DefaultLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, spelling_config=None):
        SpellingChecker.__init__(self, spelling_config)

        self.words = []
        self.sum_of_words = 0

        if spelling_config is None:
            corpus_filename = os.path.dirname(__file__) + os.sep + "corpus.txt"
        else:
            corpus_filename = spelling_config.corpus

        if os.path.exists(corpus_filename) is True:
            YLogger.info(self, "Loading spelling corpus [%s]", corpus_filename)

            self.words = Counter(self._all_words(open(corpus_filename, encoding="utf-8").read()))
            self.sum_of_words = sum(self.words.values())
        else:
            YLogger.error(self, "No spelling corpus found[%s]", corpus_filename)

    def _all_words(self, text):
        return re.findall(r'\w+', text.upper())

    def _probability(self, word):
        # Probability of `word`.dont handle null well ...
        if self.sum_of_words == 0:
            return 0.0
        return self.words[word] / self.sum_of_words

    def _correction(self, word):
        # Most probable spelling _correction for word.
        return max(self._candidates(word), key=self._probability)

    def _candidates(self, word):
        # Generate possible spelling _corrections for word.
        return self._known([word]) or self._known(self._edits1(word)) or self._known(self._edits2(word)) or [word]

    def _known(self, words):
        # The subset of `words` that appear in the dictionary of WORDS.
        return set(w for w in words if w in self.words)

    def _edits1(self, word):
        # All edits that are one edit away from `word`.
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in NorvigSpellingChecker.DefaultLetters]
        inserts = [L + c + R  for L, R in splits for c in NorvigSpellingChecker.DefaultLetters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word):
        # All edits that are two edits away from `word`.
        return (e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))

    def correct(self, phrase):
        # split sentence in into word to be check by _correction
        phras = ''
        for wrd in phrase.split():
            phras = phras+self._correction(wrd.upper())+' '
        return phras.strip()
