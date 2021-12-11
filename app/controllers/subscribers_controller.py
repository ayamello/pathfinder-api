from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.base_controller import create
from app.models.subscribers_model import SubscriberModel
from app.exceptions.activities_exception import WrongKeysError, NotFoundDataError
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError

@jwt_required()
def create_subscriber():
    try:
        data = request.get_json()
        
        new_sub = create(data, SubscriberModel, "")

        return jsonify(new_sub), 201

    except IntegrityError:
        return {'error': 'Request must contain only, user_id and path_id'}, 400
