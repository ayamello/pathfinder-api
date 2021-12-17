from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from app.controllers import create
from app.models.subscribers_model import SubscriberModel
from app.exceptions.base_exceptions import NotFoundDataError, WrongKeysError, PathOwnerError


@jwt_required()
def create_subscriber():
    try:
        data = request.get_json()
        
        current_user = get_jwt_identity()

        data['user_id'] = current_user['id']
        
        validated_data = SubscriberModel.validate(**data)
        

        new_sub = create(validated_data, SubscriberModel, "")
        return jsonify({'teste': new_sub}), 201

    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400
        
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400
    
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404
