from flask import render_template
from flask_mail import Message

from app import mail, app
from app.decorators import async
from config import ADMINS


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def password_reset_notification(user, new_password):
    send_email("[KWB] Your password has been reset!",
               ADMINS[0],
               [user.email],
               render_template("mail/password_reset_mail.txt",
                               user=user, new_password=new_password),
               render_template("mail/password_reset_mail.html",
                               user=user, new_password=new_password))


def new_account_notification(user, password):
    send_email("[KWB] Your password has been reset!",
               ADMINS[0],
               [user.email],
               render_template("mail/admin_new_user.txt",
                               user=user, password=password),
               render_template("mail/admin_new_user.html",
                               user=user, password=password))
