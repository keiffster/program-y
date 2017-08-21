#http://norvig.com/spell-correct.html

import re
import os
import logging
from collections import Counter

class SpellingChecker(object):

    DefaultLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, spelling_config=None):

        if spelling_config is None:
            corpus_filename = os.path.dirname(__file__) + os.sep + "corpus.txt"
        else:
            corpus_filename = spelling_config.corpus

        if logging.getLogger().isEnabledFor(logging.INFO): logging.info("Loading spelling corpus [%s]"%corpus_filename)
        self.words = Counter(self.all_words(open(corpus_filename).read()))
        self.sum_of_words = sum(self.words.values())

    def all_words(self, text):
        return re.findall(r'\w+', text.upper())

    def probability(self, word):
        "Probability of `word`.dont handle null well ..."
        if self.sum_of_words==0:
            return 0.0
        else:
            return self.words[word] / self.sum_of_words

    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.probability)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.words)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in SpellingChecker.DefaultLetters]
        inserts    = [L + c + R               for L, R in splits for c in SpellingChecker.DefaultLetters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def correct(self, phrase):
        "split sentence in into word to be check by correction"
        phras=''
        for wrd in phrase.split():
            phras=phras+self.correction(wrd.upper())+' '
        return phras.strip()
