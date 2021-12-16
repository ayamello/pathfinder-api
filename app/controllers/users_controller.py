from datetime import datetime, timezone
from flask import request, jsonify, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.base_exceptions import EmptyStringError, MissingKeyError, NotStringError, NotFoundDataError, WrongKeysError, EmailAlreadyExists, UsernameAlreadyExists, PasswordConfirmationDontMatch
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from app.controllers import create, delete, get_all, update
import sqlalchemy
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


    message = 'Bem vindo(a) ao PathFinder, {}! Click here to validade your acount - https://pathfinder-q3.vercel.app/confirmation/{}'.format(kwargs['username'], kwargs['email'])
    
    email.attach(MIMEText(message, 'plain'))
    context = ssl.create_default_context()
  
    with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as server:
        server.login(email['From'], password)
        server.sendmail(email['From'], email['To'], email.as_string())


def create_user():
    try:
        data = request.get_json()

        send_email(**data)

        validated_data = UserModel.validate(**data)
        
        password_to_hash = validated_data.pop('password')
        new_user = create(validated_data, UserModel, password_to_hash)
        
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except EmptyStringError as err:
        return jsonify({'error': str(err)}), 400

    except UsernameAlreadyExists as err:
        return jsonify({'error': str(err)}), 409

    except EmailAlreadyExists as err:
        return jsonify({'error': str(err)}), 409

    except MissingKeyError as err:
        return jsonify({'error': err.message}), 400

    except PasswordConfirmationDontMatch as err:
        return jsonify({'error': str(err)}), 400

    output = {
        "id": new_user.id,
        "name": new_user.name,
        "username": new_user.username,
        "email": new_user.email,
        "birthdate": new_user.birthdate.strftime("%d/%m/%Y"),
        "url_image": new_user.url_image,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at,
        "paths_lists": new_user.paths_list
    }

    return jsonify(output), 201


def login():
    activate = request.args.get('activate')

    data = request.get_json()

    found_user: UserModel = UserModel.query.filter_by(email=data['email']).first()
    
    if not found_user:
        return {'error': 'User not found'}, 404

    if activate:
        found_user.confirm_email = True
        current_app.db.session.commit()

    if found_user.confirm_email == False:
        return {'error': 'Please activate your account'}, 409
    

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
        return {'error': 'User ID not found.'}, 404

    return jsonify(user), 200
    

@jwt_required()
def update_user(id):
    try:
        data = request.get_json()
        
        data['updated_at'] = datetime.now(timezone.utc)

        user = update(UserModel, data, id)

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    return user

@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()
    admin_id = current_user['id']
    
    if admin_id != id:
        return {"error": "Unauthorized action"}

    try:
        user = delete(UserModel, id)
    
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return {'error': 'User not found.'}, 404

    return user
