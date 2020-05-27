import csv
import os
import re
from email import policy
from email.parser import BytesParser


class EmlToCSV(object):
    def get_eml(self, filePath):
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

    def change_eml_to_csv_file(self, file_path):
        if os.path.isfile('./emails.csv'):
            return './emails.csv'

        csv_file = open('./emails.csv', 'w', encoding='utf-8', newline='')
        field_names = ['subject', 'body', 'type']

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for (path, directory, files) in os.walk(file_path):
            if path is not file_path:
                dir_label = os.path.split(path)[-1]
                for file in files:
                    subject, body = self.get_eml(path + '/' + file)
                    writer.writerow({'subject': subject, 'body': body, 'type': dir_label})

        csv_file.close()
        return './emails.csv'

    def get_email_csv_file_path(self):
        if os.path.isfile('./emails.csv'):
            return './emails.csv'
        else:
            return None
