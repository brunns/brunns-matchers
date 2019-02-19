# encoding=utf-8
import email
import random
import string
from email.mime.text import MIMEText


def a_message(
    to_name=None, to_address=None, from_name=None, from_address=None, subject=None, body_text=None
):
    to_name = to_name or a_string()
    to_address = to_address or an_email_address()
    from_name = from_name or a_string()
    from_address = from_address or an_email_address()
    subject = subject or a_string()
    body_text = body_text or a_string()

    msg = MIMEText(body_text)
    msg["To"] = email.utils.formataddr((to_name, to_address))
    msg["From"] = email.utils.formataddr((from_name, from_address))
    msg["Subject"] = subject
    return msg


def an_email_address():
    return "{0}@example.com".format(a_string())


def a_string(length=10, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))
