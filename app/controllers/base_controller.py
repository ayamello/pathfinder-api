from flask import current_app, jsonify
from app.exceptions.activities_subscribers_exception import NotFoundDataError, WrongKeysError
from app.models.users_model import UserModel

def create(data, model, password_hash):
    new_item = model(**data)

    if model == UserModel:
        new_item.password = password_hash

    current_app.db.session.add(new_item)
    current_app.db.session.commit()

    return new_item


def get_all(model):
    items = model.query.all()

    return items


def update(model, data, id):
    item = model.query.get(id)

    if not item:
        raise NotFoundDataError('Id not found!')
    
    item = model.query.filter(model.id == id).update(data)

    if not item:
        raise WrongKeysError

    current_app.db.session.commit()

    updated = model.query.get(id)

    return jsonify(updated), 200


def delete(model, id):
    item = model.query.get(id)

    if not item:
        raise NotFoundDataError('Activity ID not found!')

    current_app.db.session.delete(item)
    current_app.db.session.commit()

    return '', 204
