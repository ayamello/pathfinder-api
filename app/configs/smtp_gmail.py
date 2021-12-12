from flask import Flask
from environs import Env
from flask_mail import Mail

env = Env()
env.read_env()

mail = Mail()

def init_app(app: Flask):
    app.config.update(
        MAIL_SERVER='smtp@gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TSL=True,
        MAIL_USERNAME=env('USER_EMAIL'),
        MAIL_PASSWORD=env('PASSWORD_EMAIL')
    )

    mail.init_app(app)

    return mail


def send_email():
    ...
