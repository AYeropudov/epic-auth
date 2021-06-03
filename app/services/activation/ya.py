import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from config import Config
import ssl


class ActivationService(object):
    @staticmethod
    def send(code, user):
        TO = user.email
        FROM = Config.SMTP_USER
        # create the message
        msg = MIMEMultipart()
        msg["From"] = FROM
        msg["Subject"] = 'Активация аккаунта'
        msg["To"] = TO
        msg.attach(MIMEText("Код для активации - " + code))
        HOST = "smtp.yandex.ru"

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(HOST, 465, context=context) as server:
            server.login(FROM, Config.SMTP_PASS)
            result = server.sendmail(FROM, TO, msg.as_string())