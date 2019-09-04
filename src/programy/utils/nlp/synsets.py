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
from textblob import Word
from textblob.wordnet import VERB, NOUN, ADJ, ADV


class Synsets(object):

    @staticmethod
    def _get_synsets(string, pos=None):
        if pos is None:
            word = Word(string)
            synsets = word.synsets
        else:
            word = Word(string)
            synsets = word.get_synsets(pos)

        return synsets

    @staticmethod
    def _get_lemma_and_weight(synset):
        parts = synset.name().split(".")
        return parts[0], int(parts[2])

    @staticmethod
    def get_similar_words(string, pos=None, weight=0):
        synsets = Synsets._get_synsets(string, pos)

        synset_words = []
        for synset in synsets:
            synset_lemma, synset_weight = Synsets._get_lemma_and_weight(synset)
            if synset_weight >= weight:
                if synset_lemma not in synset_words:
                    synset_words.append(synset_lemma)

        return synset_words

    @staticmethod
    def get_similar_verbs(string, weight=0):
        return Synsets.get_similar_words(string, VERB, weight=weight)

    @staticmethod
    def get_similar_nouns(string, weight=0):
        return Synsets.get_similar_words(string, NOUN, weight=weight)

    @staticmethod
    def get_similar_adjectives(string, weight=0):
        return Synsets.get_similar_words(string, ADJ, weight=weight)

    @staticmethod
    def get_similar_adverbs(string, weight=0):
        return Synsets.get_similar_words(string, ADV, weight=weight)

    @staticmethod
    def get_similarity(string1, string2, pos=None):
        syns1 = Synsets._get_synsets(string1, pos)
        syns2 = Synsets._get_synsets(string2, pos)

        similarities = []
        for syn1 in syns1:
            for syn2 in syns2:
                similarity = syn1.path_similarity(syn2)
                if similarity is not None:
                    lemma1, weight1 = Synsets._get_lemma_and_weight(syn1)
                    lemma2, weight2 = Synsets._get_lemma_and_weight(syn2)
                    similarities.append((lemma1, lemma2, similarity))

        return similarities
