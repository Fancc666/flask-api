import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.header import Header
from flask import Blueprint, request
import base64
import json

bp = Blueprint('mail', __name__, url_prefix='/api')

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

@bp.route('/mail', methods=["POST"])
def mail_api():
    res = {
        "code": 0,
        "msg": "",
        "data": []
    }
    try:
        # token
        tw = request.get_json()["to_whom"]
        sub = request.get_json()["subject"]
        ct = request.get_json()["content"]
        tk = tw + "+" + sub + "+" + ct
        tk_num = 0
        for x in tk:
            tk_num += ord(x)
        if base64.b64encode(str(tk_num).encode('utf-8')).decode('utf-8') != request.get_json()["token"]:
            res["code"] = 1
            res["msg"] = "token invalid"
        else:
            # send mail
            m = mail()
            m.message(tw, sub, ct)
            m.send()
    except Exception as e:
        res["code"] = 1
        res["msg"] = str(e)
    res_text = "api_response=" + json.dumps(res, ensure_ascii=False)
    if request.args.get("type") == "json":
        return res_text
    return res
