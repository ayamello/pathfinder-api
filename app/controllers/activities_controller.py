from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.base_controller import create, update
from app.models.activities_model import ActivityModel
from app.exceptions.activities_exception import WrongKeysError, NotFoundDataError
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError

@jwt_required()
def create_activity():
    try:
        data = request.get_json()

        new_activity = create(data, ActivityModel, "")

        return jsonify(new_activity), 201

    except IntegrityError:
        return {'error': 'Request must contain only, name, description and point_id'}, 400

@jwt_required()
def update_activity(id: int):

    try:
        data = request.get_json()

        activity = update(ActivityModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    return activity


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
        return jsonify({'error': str(err)}), 400

