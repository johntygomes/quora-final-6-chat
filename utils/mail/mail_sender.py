################################################################
from .Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
################################################################
CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
################################################################
class MailSender:
    mail_sender     = "instanalysis7@gmail.com"
    def __init__(self,mail_receiver):
        self.mail_receiver       = mail_receiver
    def sendUserAnswerNotification(self,question_object,response_object):
        self.question_object     = question_object
        self.response_object     = response_object
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        try:
            temp = f"""\
                <html>
                    <head></head>
                    <body>
                        <div style="text-align:center;margin-bottom:10px">
                            <h2>Press Button Below To Check Answer</h2>
                        </div>
                        <div style="text-align:center;margin-bottom:25px">
                            <a href="{settings.ROOTURL}/question/{str(question_object.id)}" style="font-size:15px;line-height:1.4;border-radius:3px;display:inline-block;outline:0;padding:15px 20px;text-align:center;text-decoration:none;background-color:#168de9;color:#fff;padding:15px 25px" target="_blank">
                                View Answer
                            </a>
                        </div>
                    </body>
                </html>
                """
            emailMsg = temp
            mimeMessage = MIMEMultipart()
            mimeMessage['to'] = question_object.author.email
            temp = question_object.title + " Got An Answer From:: " + response_object.username
            mimeMessage['subject'] = temp
            mimeMessage.attach(MIMEText(emailMsg, 'html'))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        except Exception as e:
            print("error",e)

class EmailVerificationMailSender:
    mail_sender     = "instanalysis7@gmail.com"
    def __init__(self,mail_receiver):
        self.mail_receiver       = mail_receiver
    def sendUserEmailVerifyMessage(self,absUrl):
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        try:
            temp = f"""\
                <html>
                    <head></head>
                    <body>
                        <div style="text-align:center;margin-bottom:10px">
                            <h2>Click Button Below To Verify Your Email</h2>
                        </div>
                        <div style="text-align:center;margin-bottom:25px">
                            <a href="{absUrl}" style="font-size:15px;line-height:1.4;border-radius:3px;display:inline-block;outline:0;padding:15px 20px;text-align:center;text-decoration:none;background-color:#168de9;color:#fff;padding:15px 25px" target="_blank">
                                Verify Email
                            </a>
                        </div>
                    </body>
                </html>
                """
            emailMsg = temp
            mimeMessage = MIMEMultipart()
            mimeMessage['to'] = self.mail_receiver.email
            temp = self.mail_receiver.username + " Verify Your Email Please"
            mimeMessage['subject'] = temp
            mimeMessage.attach(MIMEText(emailMsg, 'html'))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        except Exception as e:
            print("error",e)

class PasswordResetMailSender:
    mail_sender     = "instanalysis7@gmail.com"
    def __init__(self,mail_receiver):
        self.mail_receiver       = mail_receiver
    def sendUserPasswordResetMessage(self,absUrl):
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        try:
            temp = f"""\
                <html>
                    <head></head>
                    <body>
                        <div style="text-align:center;margin-bottom:10px">
                            <h2>Click Button Below To Verify Your Email</h2>
                        </div>
                        <div style="text-align:center;margin-bottom:25px">
                            <a href="{absUrl}" style="font-size:15px;line-height:1.4;border-radius:3px;display:inline-block;outline:0;padding:15px 20px;text-align:center;text-decoration:none;background-color:#168de9;color:#fff;padding:15px 25px" target="_blank">
                                Reset Password
                            </a>
                        </div>
                    </body>
                </html>
                """
            emailMsg = temp
            mimeMessage = MIMEMultipart()
            mimeMessage['to'] = self.mail_receiver.email
            temp = self.mail_receiver.username + " Click Link Below To Reset Your Password"
            mimeMessage['subject'] = temp
            mimeMessage.attach(MIMEText(emailMsg, 'html'))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        except Exception as e:
            print("error",e)
