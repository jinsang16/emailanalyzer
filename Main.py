
from emailparser import emlToCsv
from keywords import keywordtokenizer
from keywords import keywordanalyzer

import pandas as pd


def get_file_path():
    file_path = 'E:\EMAIL\Data\LEEJINSANG'
    return file_path


def get_words_list(data_frame):
    keywordtokenizer.load_konlpy_tokenizer("kkma")

    words = []
    for i in data_frame.index:
        val = df.loc[i, 'body']
        val = val.strip()

        if val is None or len(val) == 0:
            continue

        token = keywordtokenizer.get_konlpy_nouns(val)
        print(token)
        words.extend(token)
    return words


if __name__ == '__main__':
    # 1. Changed the email files to csv files
    file_path = get_file_path()
    csv_file_path = emlToCsv.EmlToCSV().change_eml_to_csv_file(file_path)
    print(csv_file_path)

    # 2. Read the csv file and make word list
    df = pd.read_csv(csv_file_path)
    df.dropna(axis=0, inplace=True)

    word_list = get_words_list(df)

    # 3. Count the word counts.
    frequent_words = keywordanalyzer.get_most_frequent_words(word_list, 100)