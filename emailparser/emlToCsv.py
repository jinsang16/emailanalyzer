import csv
import os
import re
from email import policy
from email.parser import BytesParser


class EmlToCSV(object):
    def get_eml(self, file_path):
        with open(file_path, 'rb') as emlFile:
            msg = BytesParser(policy=policy.default).parse(emlFile)

            if msg.get_body(preferencelist='html') is not None:
                body = msg.get_body(preferencelist='html').get_content()
            elif msg.get_payload(decode=True) is not None:
                body = msg.get_payload(decode=True).decode('UTF-8')
            else:
                body = ''
            body = re.split('-*\s*Original Message', body)[0]
            pattern = '<head.*/head>|<style.*/style>|<!-.+?->|<.+?>|&nbsp;|\t|\r|\u200b'
            body = re.sub(pattern, '', body, 0, re.I | re.S)
            # body = ' '.join(body.splitlines())

            return msg['Date'], msg['Subject'], body

    def change_eml_to_csv_file(self, file_path):
        if os.path.isfile('./emails.csv'):
            return './emails.csv'

        csv_file = open('./emails.csv', 'w', encoding='utf-8-sig', newline='')
        field_names = ['received_date', 'subject', 'body']

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for (path, directory, files) in os.walk(file_path):
            for file in files:
                if file.endswith('.eml'):
                    date, subject, body = self.get_eml(path + '/' + file)
                    if body.isspace() is False:
                        writer.writerow({'received_date': date, 'subject': subject, 'body': body})
        csv_file.close()
        return './emails.csv'

    def get_email_csv_file_path(self):
        if os.path.isfile('./emails.csv'):
            return './emails.csv'
        else:
            return None
