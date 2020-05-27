import csv
import os
import re
from email import policy
from email.parser import BytesParser


def get_eml(filePath):
    with open(filePath, 'rb') as emlFile:
        msg = BytesParser(policy=policy.default).parse(emlFile)

        if msg.get_body(preferencelist='html') is not None:
            text = msg.get_body(preferencelist='html').get_content()
        elif msg.get_payload(decode=True) is not None:
            text = msg.get_payload(decode=True).decode('UTF-8')
        else:
            text = ''
        text = re.sub('<head.*/head>|<style.*/style>|<!-.+?->|<.+?>|&nbsp;|\t|\r', '', text, 0, re.I | re.S)
        text = ''.join(text.splitlines())

        return msg['Subject'], text


def make_csv_from_eml(dirPath):
    csv_file = open('./emails.csv', 'w', encoding='utf-8', newline='')
    field_names = ['subject', 'body', 'type']
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for (path, directory, files) in os.walk(dirPath):
        if path is not dirPath:
            dirLabel = os.path.split(path)[-1]
            for file in files:
                subject, body = get_eml(path + '/' + file)
                writer.writerow({'subject': subject, 'body': body, 'type': dirLabel})

    csv_file.close()
