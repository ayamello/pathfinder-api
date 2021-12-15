from flask import request, jsonify
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required
from app.controllers.__init__ import create, delete, update
from app.models.reviews_model import ReviewModel
from app.models.activities_model import ActivityModel
from app.exceptions.base_exceptions import NotStringError, WrongKeysError, NotFoundDataError
from sqlalchemy.exc import InvalidRequestError


@jwt_required()
def create_review():
    try:
        data = request.get_json()

        validated_data = ReviewModel.validate(**data)

        new_review = create(validated_data, ReviewModel, '')

        return jsonify(new_review), 201

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400


@jwt_required()
def reviews_by_activity(activity_id: int):
    try:
        activity = ActivityModel.query.get(activity_id)
        return {'reviews': activity.reviews}, 200
    except AttributeError:
        return {'error': 'Activity ID Not Found'}, 404


@jwt_required()
def update_review(id: int):
    try:
        data = request.get_json()

        data['updated_at'] = datetime.now(timezone.utc)

        review = update(ReviewModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    except InvalidRequestError as err:
        return jsonify({'error': str(err)}), 400

    return review


@jwt_required()
def delete_review(id: int):
    try:
        review = delete(ReviewModel, id)

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    return review
