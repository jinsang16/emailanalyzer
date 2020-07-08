import pandas as pd

from emailparser import emlToCsv
from keywords import keywordanalyzer
from keywords import keywordtokenizer
from pattern import invitedchecker


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
    data_frame['subject'] = data_frame['subject'].astype(str)
    subject_list = list(map(lambda x: x.upper(), data_frame['subject'].values))

    for i in data_frame.index:
        subject = data_frame.loc[i, 'subject']
        subject = 'RE: ' + subject.upper()

        if subject in subject_list:
            data_frame.loc[i, 'labelled'] = 1
            print(data_frame.loc[i, 'subject'])
            print('This subject has a reply name.')

    return data_frame


if __name__ == '__main__':
    # 1. Changed the email files to csv files
    file_path = get_file_path()
    csv_file_path = emlToCsv.EmlToCSV().change_eml_to_csv_file(file_path)
    print(csv_file_path)

    # 2. Read the csv file and drop unnecessary data
    df = pd.read_csv(csv_file_path)
    df.dropna(subset=['body'], axis=0, inplace=True)
    df.drop_duplicates(subset=['subject'], inplace=True)

    df = add_labelled_columns(df)
    df.to_csv('E:\EMAIL\Data\LEEJINSANG\emails.csv', encoding='utf-8-sig', index=None)

    # 3. Make word list
    word_list = get_words_list(df.loc[df['labelled'] > 0])

    # 4. Count the word counts.
    frequent_words = keywordanalyzer.get_most_frequent_words(word_list, 99999)
    print('frequent_words:', frequent_words)

    # check invited mail
    df = invitedchecker.add_invited_col(df)
    df = invitedchecker.get_invited_date(df)
    df.to_csv('E:\EMAIL\Data\LEEJINSANG\emails.csv', encoding='utf-8-sig', index=None)
    # print(df.loc[df['invited'] > 0])
