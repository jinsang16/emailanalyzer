import re

import pandas as pd


def get_split_subject(data):
    text = re.sub('RE: +|RE:|FW: +|FW:', '', data['subject'], 0, re.I | re.S)
    return text


'''
Main
'''
df = pd.read_csv('./emails.csv')
inboxData = df.loc[df['type'].str.contains('Inbox'), ['subject', 'body']]

splitData = df.loc[df['type'].str.contains('Sent'), ['subject']]
splitData = splitData.apply(get_split_subject, axis=1)

inboxData['reply'] = 0
for split in splitData:
    mask = inboxData.subject.str.endswith(split)
    inboxData.loc[mask, 'reply'] = 1

print(inboxData.loc[inboxData['reply'] > 0, ['subject', 'reply']])
inboxData.to_csv('./replyCheck.csv')
