from flask import request, jsonify
from app.exceptions.activities_subscribers_exception import NotFoundDataError, WrongKeysError
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from app.controllers.base_controller import create, delete, get_all, update
import sqlalchemy
import psycopg2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from os import environ


def send_email(**kwargs):
    email = MIMEMultipart()
    password = environ.get('SMTP_PASS')
    
    email['From'] = environ.get('STMP_MAIL')
    email['To'] = kwargs['email']
    email['Subject'] = 'Boas vindas'

    message = 'Bem vindo(a) ao PathFinder!'
    
    email.attach(MIMEText(message, 'plain'))
    context = ssl.create_default_context()
  
    with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as server:
        server.login(email['From'], password)
        server.sendmail(email['From'], email['To'], email.as_string())


def create_user():
    try:
        data = request.get_json()

        send_email(**data)

        password_to_hash = data.pop('password')
        
        new_user = create(data, UserModel, password_to_hash)

        

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'error': 'There are fields missing.'}, 400

        return {'error': 'This user already exists.'}, 409

    except TypeError as e:
        return {'error': 'There are extra fields.'}, 400

    return jsonify(new_user), 201


def login():
    data = request.get_json()

    found_user: UserModel = UserModel.query.filter_by(email=data['email']).first()

    if not found_user:
        return {'error': 'User not found'}, 404

    if found_user.verify_password(data['password']):
        access_token = create_access_token(identity=found_user)
        return {
            'token': access_token
            }, 200
    else:
        return {'error': 'Unauthorized'}, 401


@jwt_required()
def get_all_users():
    users = get_all(UserModel)

    return jsonify(users), 200


@jwt_required()
def get_by_id(id):
    user = UserModel.query.get(id)

    if not user:
        return {'error': 'User not found.'}, 404

    return jsonify(user), 200
    

@jwt_required()
def update_user(id):
    try:
        data = request.get_json()

        user = update(UserModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    return user


@jwt_required()
def delete_user(id):
    try:
        user = delete(UserModel, id)
    
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return {'error': 'User not found.'}, 404

    return user
