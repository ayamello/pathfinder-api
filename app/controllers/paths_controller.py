from flask import request, current_app, jsonify
from app.controllers.base_controller import create, get_all, update
from app.exceptions.activities_exception import NotFoundDataError, WrongKeysError
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def create_path():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']

        path = create(data, PathModel, "")

        result = {
            "id": path.id,
            "name": path.name,
            "description": path.description,
            "initial_date": path.initial_date,
            "end_date": path.end_date,
            "duration": path.duration,
            "user": {
                "name": path.user.name,
                "email": path.user.email
            }
        }

        return jsonify(result), 201

    except:
        return jsonify({'error': 'error'}), 400

@jwt_required()
def delete_path(id):
    try:
        path_to_delete = PathModel.query.filter_by(id=id).first()
        current_app.db.session.delete(path_to_delete)
        current_app.db.session.commit()
        return '', 204
    except UnmappedInstanceError:
        return {'msg': 'Path ID Not Found'}, 404

def update_path(id):

    # Se não for string 
    # se a string estiver vazia
    # keys incorretas
    # não poderia trocar o user_id
    # end date não pode ser uma data antes, só depois
    try:
        data = request.get_json()

        path = update(PathModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    return path

def get_all_paths():

    paths = get_all(PathModel)
    
    return jsonify(paths), 200

def get_paths_by_user_id(id):
    # tratar lista vazia
    # paginação da rota
    paths_by_user = PathModel.query.filter_by(user_id=id).all()

    return jsonify(paths_by_user), 200

# update
# get by id do usuario
# get geralzao