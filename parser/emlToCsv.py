import csv
import os
import re
from email import policy
from email.parser import BytesParser


def get_eml(filePath):
    with open(filePath, 'rb') as emlFile:
        msg = BytesParser(policy=policy.default).parse(emlFile)

        if msg.get_body(preferencelist='html') is not None:
            body = msg.get_body(preferencelist='html').get_content()
        elif msg.get_payload(decode=True) is not None:
            body = msg.get_payload(decode=True).decode('UTF-8')
        else:
            body = ''
        body = re.sub('<head.*/head>|<style.*/style>|<!-.+?->|<.+?>|&nbsp;|\t|\r', '', body, 0, re.I | re.S)
        body = ''.join(body.splitlines())

        return msg['Subject'], body


'''
Main
'''
myDir = 'D:/05_PythonProject/emailanalyzer/eml/'  # TODO 프로젝트 경로에 맞게 수정 필요!
csvFile = open('./emails.csv', 'w', encoding='utf-8', newline='')
fieldNames = ['subject', 'body', 'type']
writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
writer.writeheader()

for (path, directory, files) in os.walk(myDir):
    if path is not myDir:
        dirLabel = os.path.split(path)[-1]
        for file in files:
            subject, body = get_eml(path + '/' + file)
            writer.writerow({'subject': subject, 'body': body, 'type': dirLabel})

csvFile.close()
