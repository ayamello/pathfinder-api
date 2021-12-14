from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.__init__ import create
from app.models.subscribers_model import SubscriberModel
from app.exceptions.activities_subscribers_exception import WrongKeysError, PathOwnerError


@jwt_required()
def create_subscriber():
    try:
        data = request.get_json()
        
        validated_data = SubscriberModel.validate(**data)

        new_sub = create(validated_data, SubscriberModel, "")

        return jsonify(new_sub), 201

    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400
