
import re
import pickle
import sys
from collections import Counter

if __name__ == '__main__':

    def all_words(text):
        return re.findall(r'\w+', text.upper())

    def create_corpus(text_filename, corpus_filename):

        words = Counter(all_words(open(text_filename).read()))
        sum_of_words = sum(words.values())

        corpus = (words, sum_of_words)
        with open(corpus_filename, "wb+") as f:
            pickle.dump(corpus, f)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    create_corpus(input_file, output_file)