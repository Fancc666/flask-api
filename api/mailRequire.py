import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.header import Header

class mail:
    def __init__(self) -> None:
        self.connect = smtplib.SMTP_SSL("smtp.163.com")
        self.connect.login("verify565455@163.com", "NNBOICXHBYQHUCCL")
    def message(self, to_whom, subject, content):
        self.to_whom = to_whom
        self.subject = subject
        self.content = content
        # 邮件主体
        self.msg = MIMEMultipart()
        # 设置邮件主题
        self.subject = Header(subject, 'utf-8').encode()
        self.msg['Subject'] = subject
        # 设置邮件发送者
        self.msg['From'] = 'verify565455@163.com <verify565455@163.com>'
        # 设置邮件接受者
        self.msg['To'] = to_whom
        # 添加⽂文字内容
        text = MIMEText(content, 'plain', 'utf-8') 
        self.msg.attach(text)
    def send(self):
        self.connect.sendmail('verify565455@163.com', self.to_whom, self.msg.as_string()) 
        self.connect.quit()
