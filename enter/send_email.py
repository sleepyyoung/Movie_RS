import smtplib
from email.mime.text import MIMEText
from email.header import Header
from Movie_RS import settings


class Mail:
    def __init__(self, receiver, captcha, method):
        self.mail_host = settings.EMAIL_HOST  # "smtp.qq.com"
        self.mail_port = settings.EMAIL_PORT  # 465
        self.mail_pass = settings.EMAIL_HOST_PASSWORD  # "reivzpjdtrffcjdc"
        self.sender = settings.EMAIL_HOST_USER  # "1696589321@qq.com"
        self.from_ = settings.EMAIL_FROM  # "微博历史热搜"
        self.receiver = receiver  # self.receivers = [receiver]
        self.captcha = captcha
        self.method = "注册" if method == "register" else "忘记密码"  # forgot_password

    def send(self):
        mail_msg = f"""
        <p>您正在电影推荐系统网站 </a> 利用该邮箱账号进行{self.method}操作</p>
        <p>验证码为 <strong><font size="50px"> {self.captcha} </font></strong></p>
        <p>有效时间5分钟</p>
        <p>如非本人操作，请忽略</p>
        """
        message = MIMEText(mail_msg, 'html', 'utf-8')

        message['From'] = Header(self.from_, 'utf-8')
        message['To'] = Header(self.receiver, 'utf-8')

        message['Subject'] = Header(f"电影推荐系统-{self.method}", 'utf-8')

        smtp_obj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
        smtp_obj.login(self.sender, self.mail_pass)
        smtp_obj.sendmail(self.sender, self.receiver, message.as_string())
        smtp_obj.quit()

# if __name__ == '__main__':
#     mail = Mail(receiver="1696589321@qq.com", captcha="123466", method="注册")
#     mail.send()
