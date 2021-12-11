from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.models.subscribers_model import SubscriberModel
from app.exceptions.activities_subscribers_exception import WrongKeysError, PathOwnerError

@jwt_required()
def create_subscriber():
    try:
        data = request.get_json()
        validated_data = SubscriberModel.validate(**data)
        subscriber = SubscriberModel(**validated_data)
        current_app.db.session.add(subscriber)
        current_app.db.session.commit()

        return jsonify(validated_data), 201
    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400
