from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.models.activities_model import ActivityModel
from app.exceptions.activities_subscribers_exception import NotStringError, WrongKeysError, NotFoundDataError
from sqlalchemy.exc import InvalidRequestError

@jwt_required()
def create_activity():
    try:
        data = request.get_json()
        validated_data = ActivityModel.validate(**data)
        activity = ActivityModel(**validated_data)
        current_app.db.session.add(activity)
        current_app.db.session.commit()

        return jsonify(activity), 201
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400
    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

@jwt_required()
def update_activity(id: int):
    try:
        data = request.get_json()
        activity = ActivityModel.query.get(id)
        if not activity:
            raise NotFoundDataError('Activity ID not found!')
        activity = ActivityModel.query.filter(ActivityModel.id == id).update(data)

        current_app.db.session.commit()

        updated_activity = ActivityModel.query.get(id)

        return jsonify(updated_activity), 200
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404
    except InvalidRequestError as err:
        return jsonify({"error": str(err)}), 400


@jwt_required()
def delete_activity(id: int):
    try:
        activity = ActivityModel.query.get(id)
        if not activity:
            raise NotFoundDataError('Activity ID not found!')

        current_app.db.session.delete(activity)
        current_app.db.session.commit()

        return '', 204
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

