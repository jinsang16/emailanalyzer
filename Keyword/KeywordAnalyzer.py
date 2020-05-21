# import Keyword.KeywordTokenizer
from collections import Counter


def get_most_frequent_words(words, words_count):
    count = Counter(words)
    word_dic = {}

    for w, c in count.most_common(words_count):
        if 2 <= len(w) <= 49:
            word_dic[w] = c

    return word_dic


