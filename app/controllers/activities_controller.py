from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.base_controller import create, delete, update
from app.models.activities_model import ActivityModel
from app.exceptions.activities_subscribers_exception import NotStringError, WrongKeysError, NotFoundDataError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from app.models.points_model import PointModel


@jwt_required()
def create_activity():
    try:
        data = request.get_json()

        validated_data = ActivityModel.validate(**data)

        new_activity = create(validated_data, ActivityModel, '')

        return jsonify(new_activity), 201

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400


@jwt_required()
def activities_by_point(path_id: int):
    try:
        point = PointModel.query.get(path_id)
        return {'activities': point.activities}, 200
    except AttributeError:
        return {'error': 'Point ID Not Found'}, 404


@jwt_required()
def update_activity(id: int):
    try:
        data = request.get_json()
        activity = update(ActivityModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    except InvalidRequestError as err:
        return jsonify({'error': str(err)}), 400

    return activity


@jwt_required()
def delete_activity(id: int):
    try:
        activity = delete(ActivityModel, id)

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    return activity
