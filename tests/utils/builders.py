# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import email
import random
import string
from email.mime.text import MIMEText


def a_message(to_name=None, to_email=None, from_name=None, from_email=None, subject=None, body_text=None):
    to_name = to_name or a_string()
    to_email = to_email or an_email_address()
    from_name = from_name or a_string()
    from_email = from_email or an_email_address()
    subject = subject or a_string()
    body_text = body_text or a_string()

    msg = MIMEText(body_text)
    msg["To"] = email.utils.formataddr((to_name, to_email))
    msg["From"] = email.utils.formataddr((from_name, from_email))
    msg["Subject"] = subject
    return msg


def an_email_address():
    return "{0}@example.com".format(a_string())


def a_string(length=10, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))
