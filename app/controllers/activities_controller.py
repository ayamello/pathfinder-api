from flask import request, current_app, jsonify
from app.models.activities_model import ActivityModel
from app.exceptions.activities_exception import WrongKeysError, NotFoundDataError
from psycopg2.errors import NotNullViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func

def create():
    try:
        data = request.get_json()
        # validated_data = ActivityModel.validate(**data)
        new_data = ActivityModel(**data)
        print(new_data)
        current_app.db.session.add(new_data)
        current_app.db.session.commit()

        return jsonify(new_data), 201
    except IntegrityError as err:
        if type(err.orig) == NotNullViolation:
            return {'Error': 'Request must contain, name, description and point_id'}, 422
    # except WrongKeysError as err:
    #     return jsonify({"error": err.message}), 404

    # if type(err.orig) == ForeignKeyViolation:
    #     return {'msg': str(e.orig).split('\n')[1]}, 422

def update(id: int):
    try:
        data = request.get_json()
        activity = ActivityModel.query.get(id)
        if not activity:
            raise NotFoundDataError('Activity not found!')
        # validated_data = ActivityModel.validate(**data)
        activity = ActivityModel.query.filter(ActivityModel.id == id).update(data)
        
        current_app.db.session.commit()

        updated_activity = ActivityModel.query.get(id)

        return jsonify(updated_activity), 200
    except NotFoundDataError as err:
        return jsonify({'Message': str(err)}), 400
    except WrongKeysError as err:
        return jsonify({'Message': err.message}), 404


def delete(id: int):
    try:
        activity = ActivityModel.query.get(id)
        if not activity:
            raise NotFoundDataError('Activity not found!')

        current_app.db.session.delete(activity)
        current_app.db.session.commit()

        return '', 204
    except NotFoundDataError as err:
        return jsonify({'Message': str(err)}), 400
