from konlpy.tag import Komoran, Okt, Hannanum, Kkma


def get_konlpy_tokenizer(tokenizer_name):
    if tokenizer_name == "okt":
        tokenizer = Okt()
    elif tokenizer_name == "hannanum":
        tokenizer = Hannanum()
    elif tokenizer_name == "kkma":
        tokenizer = Kkma()
    else:
        tokenizer = Komoran()
    return tokenizer


def get_konlpy_tokens(text, tokenizer_name="komoran"):
    tokenizer = get_konlpy_tokenizer(tokenizer_name)
    tokens = tokenizer.morphs(text)
    return tokens


def get_konlpy_pos_tagging_token(text, tokenizer_name="komoran"):
    tokenizer = get_konlpy_tokenizer(tokenizer_name)
    pos_tagging_token = tokenizer.pos(text)
    return pos_tagging_token


def remove_words_by_pos(text, remove_pos_list, tokenizer_name="komoran"):
    token = get_konlpy_pos_tagging_token(text, tokenizer_name)
    necessary_words = []

    for word in token:
        if word[1] not in remove_pos_list:
            necessary_words.append(word[0])

    return necessary_words