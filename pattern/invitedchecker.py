import re
from datetime import datetime


def add_invited_col(data_frame):
    data_frame['invited'] = 0
    data_frame['subject'] = data_frame['subject'].astype(str)

    except_pattern = '회의록|답장\s?:|전달\s?:|[Rr][Ee]\s?:|\[[Rr][Ee]\]|[Ff][Ww][Dd]\s?:|[Ff][Ww]\s?:|\[[Ff][Ww]\]'
    expected_pattern = '회의|미팅'
    for i in data_frame.index:
        subject = data_frame.loc[i, 'subject']
        reply_or_forward = re.search(except_pattern, subject)

        if reply_or_forward is None:  # reply / forward 아닐 때
            invited = re.search(expected_pattern, subject)
            if invited is not None:  # 제목에 회의, 미팅이 명시되어 있을 때
                data_frame.loc[i, 'invited'] = 1

    return data_frame


def get_invited_date(data_frame):
    data_frame['invited_date'] = None
    date_pattern = '\d{1,2}\/\d{1,2}|\d{1,2}월\s?\d{1,2}일'
    time_pattern = '\d{1,2}:\d{1,2}|\d{1,2}시\s?\d{2}분|\d{1,2}시'

    for i in data_frame.index:
        if data_frame.loc[i, 'invited'] == 0:
            continue

        subject = data_frame.loc[i, 'subject']

        # 정규식 패턴에 맞는 날짜 추출
        date = re.search(date_pattern, subject)
        if date is None:
            body = data_frame.loc[i, 'body']
            date = re.search(date_pattern, body)
        if date is not None:
            date = date.group()

        # 정규식 패턴에 맞는 시간 추출
        time = re.search(time_pattern, subject)
        if time is None:
            body = data_frame.loc[i, 'body']
            time = re.search(time_pattern, body)
        if time is not None:
            time = time.group()

        # 날짜는 Y-m-d, 시간은 H:M 으로 저장..
        received_date = re.sub('\s\+\d{4}', '', data_frame.loc[i, 'received_date'])
        received_date = datetime.strptime(received_date, '%a, %d %b %Y %H:%M:%S')
        if date is None:
            if time is not None:  # 회의 날짜는 오늘, 시간은 추출된 정보로 적용
                date = received_date.strftime('%Y/%m/%d')
                time = pick_out_invited_time(time)
        else:
            if time is None:  # 시간은 사용자가 설정할 것으로 판단
                date = pick_out_invited_date(received_date, date)
                time = '00:00'
            else:  # 날짜, 시간 모두 존재
                date = pick_out_invited_date(received_date, date)
                time = pick_out_invited_time(time)

        if date is None:
            data_frame.loc[i, 'invited'] = 0
            continue

        received = datetime.strptime(received_date.strftime('%Y/%m/%d'), '%Y/%m/%d')
        invited = datetime.strptime(date, '%Y/%m/%d')
        if received > invited:
            data_frame.loc[i, 'invited'] = 0
        else:  # 날짜, 시간 data_frame 에 저장
            data_frame.loc[i, 'invited_date'] = date + ' ' + time

    return data_frame


def pick_out_invited_date(received_date, text):
    if re.search(r'\d{1,2}월\s?\d{1,2}일', text):
        text = re.sub(r'(?P<month>\d{1,2})월\s?(?P<day>\d{1,2})일', '\g<month>/\g<day>', text)

    result = text.split('/')
    month = int(result[0])
    if 0 < month < 12:
        year = int(received_date.strftime('%Y'))
        received_month = int(received_date.strftime('%m'))
        if received_month == 12 and month == 1:  # 오늘은 12월인데 미팅날짜가 1월이면 내년이라고 판단
            year += 1
        return '%d/%02d/%02d' % (year, month, int(result[1]))
    return None


def pick_out_invited_time(text):
    if re.search(r'\d{1,2}시\s?\d{2}분', text):
        text = re.sub(r'(?P<hour>\d{1,2})시\s?(?P<min>\d{2})분', '\g<hour>:\g<min>', text)
    elif re.search(r'\d{1,2}시', text):
        text = re.sub(r'(?P<hour>\d{1,2})시', '\g<hour>:00', text)

    result = text.split(':')
    hour = int(result[0])
    if 0 < hour < 8:  # 정규근무시간 8 to 6 기준으로 저녁 시간 감안하여 0 ~ 8시 표현은 오후로 판단 7시 일정이 애매....
        hour += 12
    return '%02d:%02d' % (hour, int(result[1]))
