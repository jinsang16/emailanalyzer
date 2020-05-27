from emlParser import emlToCsv, replyChecker

# eml 파일 파싱해서 csv 만들기
dirPath = 'D:/05_PythonProject/emailanalyzer/eml/'  # TODO 프로젝트 경로에 맞게 수정 필요!
emlToCsv.make_csv_from_eml(dirPath)

# reply 여부 확인해서 csv 만들기
replyChecker.make_reply_check()
