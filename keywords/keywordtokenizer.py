from konlpy.tag import Komoran, Okt, Hannanum, Kkma

KOMORAN_NECESSARY_POS = ['NNG', 'NNP', 'NNB', 'SL', 'SH', 'NF']
KKMA_NECESSARY_POS = ['NNG', 'NNP', 'NNB', 'NNM', 'UN', 'OL', 'OH']


def load_konlpy_tokenizer(tokenizer_name):
    global tokenizer
    tokenizer = Komoran()

    if tokenizer_name == "okt":
        tokenizer = Okt()
    elif tokenizer_name == "hannanum":
        tokenizer = Hannanum()
    elif tokenizer_name == "kkma":
        tokenizer = Kkma()


def get_konlpy_tokens(text):
    tokens = tokenizer.morphs(text)
    return tokens


def get_konlpy_pos_tagging_token(text):
    pos_tagging_token = tokenizer.pos(text)
    return pos_tagging_token


def get_konlpy_nouns(text):
    nouns = tokenizer.nouns(text)
    return nouns


def remove_words_by_pos(text, remove_pos_list):
    token = get_konlpy_pos_tagging_token(text)
    necessary_words = []

    for word in token:
        if word[1] not in remove_pos_list:
            necessary_words.append(word[0])

    return necessary_words