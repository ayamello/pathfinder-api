from flask import Flask
from environs import Env
from flask_mail import Mail

env = Env()
env.read_env()

mail = Mail()

def init_app(app: Flask):
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USE_SSL']=True
    app.config['MAIL_USERNAME']=env('USER_EMAIL')
    app.config['MAIL_PASSWORD']=env('PASSWORD_EMAIL')
    app.config['MAIL_DEFAULT_SENDER']=env('USER_EMAIL')

    mail.init_app(app)


def send_email():
    ...
