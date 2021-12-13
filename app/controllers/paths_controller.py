from flask import request, jsonify
from app.controllers.base_controller import create, delete, get_all, update
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_path():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']

        path = create(data, PathModel, '')

        result = {
            "id": path.id,
            "name": path.name,
            "description": path.description,
            "initial_date": path.initial_date.strftime("%d/%m/%Y"),
            "end_date": path.end_date.strftime("%d/%m/%Y"),
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
        path = delete(PathModel, id)

    except UnmappedInstanceError:
        return {'error': 'Path ID Not Found'}, 404

    return path


def update_path(id):
    # Se não for string 
    # se a string estiver vazia
    # keys incorretas
    # não poderia trocar o user_id
    # end date não pode ser uma data antes, só depois
    data = request.get_json()

    path = update(PathModel, data, id)

    return path


def get_all_paths():
    paths = get_all(PathModel)
    #  tratar lista vazia
    # paginação da rota
    #set_trace()

    ## Ideia de serialização para mostrar apenas usernames na resposta do get:
    serializer = [{
        'id': path.id,
        'name': path.name,
        'description': path.description,
        'initial_date': path.initial_date,
        'end_date': path.end_date,
        'duration': path.duration,
        'subscribers': [{'username': user.users.username} for user in path.subscribers]
    } for path in paths]
    
    return jsonify(paths), 200


def get_paths_by_user_id(id):
    # tratar lista vazia
    # paginação da rota
    paths_by_user = PathModel.query.filter_by(user_id=id).all()

   

    return jsonify(paths_by_user), 200

# update
# get by id do usuario
# get geralzao