
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


def add_labelled_columns(data_frame):
    data_frame['labelled'] = 0
    subject_list = list(data_frame['subject'].values)

    for i in data_frame.index:
        subject = data_frame.loc[i, 'subject']
        subject = 'RE: ' + subject

        if subject in subject_list:
            data_frame.loc[i, 'labelled'] = 1
            print(subject)
            print('This subject has a reply name.')

    return data_frame

if __name__ == '__main__':
    # 1. Changed the email files to csv files
    file_path = get_file_path()
    csv_file_path = emlToCsv.EmlToCSV().change_eml_to_csv_file(file_path)
    print(csv_file_path)

    # 2. Read the csv file and make word list
    df = pd.read_csv(csv_file_path)
    df.dropna(axis=0, inplace=True)

    df = add_labelled_columns(df)
    df.to_csv('E:\EMAIL\Data\LEEJINSANG\emails.csv', encoding='utf-8-sig')

    word_list = get_words_list(df)

    # 3. Count the word counts.
    frequent_words = keywordanalyzer.get_most_frequent_words(word_list, 100)