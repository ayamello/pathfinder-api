from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.models.subscribers_model import SubscriberModel
from app.exceptions.activities_exception import WrongKeysError, NotFoundDataError
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError

@jwt_required()
def create_subscriber():
    try:
        data = request.get_json()
        new_data = SubscriberModel(**data)
        current_app.db.session.add(new_data)
        current_app.db.session.commit()

        return jsonify(new_data), 201
    except IntegrityError:
        return {'error': 'Request must contain only, user_id and path_id'}, 400
