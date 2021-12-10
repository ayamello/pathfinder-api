from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.models.activities_model import ActivityModel
from app.exceptions.activities_exception import WrongKeysError, NotFoundDataError
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError

@jwt_required()
def create_activity():
    try:
        data = request.get_json()
        print(data)
        new_data = ActivityModel(**data)
        current_app.db.session.add(new_data)
        current_app.db.session.commit()

        return jsonify(new_data), 201
    except IntegrityError:
        return {'error': 'Request must contain only, name, description and point_id'}, 400

@jwt_required()
def update_activity(id: int):
    try:
        data = request.get_json()
        activity = ActivityModel.query.get(id)
        if not activity:
            raise NotFoundDataError('Activity not found!')
        activity = ActivityModel.query.filter(ActivityModel.id == id).update(data)

        current_app.db.session.commit()

        updated_activity = ActivityModel.query.get(id)

        return jsonify(updated_activity), 200
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 400
    except WrongKeysError as err:
        return jsonify({'error': err.message}), 404


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

