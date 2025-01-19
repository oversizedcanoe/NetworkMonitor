import base64
from logging import getLogger
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
from dotenv import load_dotenv

__logger = getLogger(__name__)
load_dotenv('email.env')

port = 465
email = os.getenv('EMAIL')
hashed_password = os.getenv('PASSWORD')

def send_email(subject: str, contents: str):
    __logger.debug('Sending email: %s', subject)
    try:
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = email
        message["To"] = email
        message.attach(MIMEText(contents, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, get_password())
            server.sendmail(email, email, message.as_string()) 
    except Exception as e:
        __logger.error('Failed to send email')
        error = traceback.format_exc()
        __logger.error(error)

def get_password():
    result_bytes = base64.b64decode(hashed_password)
    result_string = result_bytes.decode('utf-8')
    return result_string
