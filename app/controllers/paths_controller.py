from flask import request, jsonify, current_app
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError


def create_path():
    data = request.get_json()

    path = PathModel(**data)
    current_app.db.session.add(path)
    current_app.db.session.commit()

    return jsonify(path), 201

def delete_path(id):
    try:
        path_to_delete = PathModel.query.filter_by(id=id).first()
        current_app.db.session.delete(path_to_delete)
        current_app.db.session.commit()
        return '', 204
    except UnmappedInstanceError:
        return {'msg': 'ID Not Found'}, 404

